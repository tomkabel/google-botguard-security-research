"""Title/abstract screening of the §3.1 rerun set (docs/corpus.csv) by two independent LLM screeners.

  python3 analysis/screen_corpus.py fetch        # abstracts -> analysis/cache/abstracts.json (Semantic Scholar batch API)
  python3 analysis/screen_corpus.py screen       # both screeners on every record -> analysis/cache/screen-<model>.json
  python3 analysis/screen_corpus.py report       # Cohen's kappa, disagreements -> docs/screening.md
  python3 analysis/screen_corpus.py apply        # merge screening + adjudication (docs/adjudication.csv) into docs/corpus.csv
  python3 analysis/screen_corpus.py code         # both models code the includes into the paper's taxonomy -> analysis/cache/coding.json
  python3 analysis/screen_corpus.py --selfcheck

Screeners are two models from different vendors on the Melious API (MELIOUS_API_KEY), temperature 0, same prompt,
blind to each other. Disagreements go to a third reader (docs/adjudication.csv). Records whose abstract could not be
retrieved are screened on title alone and flagged.
"""
import csv, json, os, re, sys, time, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CACHE = os.path.join(ROOT, "analysis", "cache")
CORPUS = os.path.join(ROOT, "docs", "corpus.csv")
SCREENERS = ["glm-5.3-flash", "mistral-small-4-119b-instruct"]
URL = "https://api.melious.ai/v1/chat/completions"

CRITERIA = """You screen records for a systematization-of-knowledge paper on CLIENT-SIDE ANTI-AUTOMATION on the web
(mechanisms that run in or are enforced through the user's browser/device to impose cost on automated clients) and on
attacks against it, especially by vision-language-model / LLM web agents.

INCLUDE if the record is peer-reviewed or preprint research that does at least one of:
 M: documents or evaluates a client-side anti-automation mechanism: CAPTCHAs/challenges (text, image, audio, behavioral),
    JavaScript/VM challenges, browser or device fingerprinting used for bot detection, behavioral biometrics
    (mouse/keystroke/touch/sensor) for bot detection, anonymous attestation tokens (Privacy Pass, Private Access Tokens),
    device-bound credentials used against automation;
 A: evaluates an automated attack on such a mechanism (CAPTCHA solvers incl. ML/LLM/VLM, web or GUI agents facing
    bot detection, fingerprint spoofing / anti-detect browsers, bot-detection evasion);
 E: measures the economics or ecosystem of bypassing such mechanisms (solver farms, bot markets).
EXCLUDE: social-media bot / sockpuppet account detection from posts or graphs; botnet or network-traffic/server-log-only
bot detection; chatbots/conversational agents; malware/phishing unrelated to anti-automation; CAPTCHA or bot work
outside the web (e.g. games) unless it transfers directly; pure proposals with no evaluation; non-research items.

Answer with exactly one JSON object and nothing else:
{"decision": "include" or "exclude", "category": "M" or "A" or "E" or "-", "reason": "<= 15 words"}"""


def http(url, data=None, headers=None, timeout=120):
    req = urllib.request.Request(url, data=data, headers={"User-Agent": "sok-screening/1.0", **(headers or {})})
    return json.loads(urllib.request.urlopen(req, timeout=timeout).read())


def load_corpus():
    with open(CORPUS, newline="") as f:
        return list(csv.DictReader(f))


def s2_id(rid):
    if rid.startswith("doi:"):
        return "DOI:" + rid[4:]
    if rid.startswith("arXiv:"):
        return "ARXIV:" + re.sub(r"v\d+$", "", rid[6:])
    return rid[3:] if rid.startswith("s2:") else rid


def openalex(rows):
    """Fallback for records Semantic Scholar did not return: OpenAlex by DOI (abstract is an inverted index)."""
    out = {}
    dois = [r["id"][4:] for r in rows if r["id"].startswith("doi:")]
    for i in range(0, len(dois), 40):
        q = "|".join("https://doi.org/" + d for d in dois[i:i + 40])
        try:
            res = http("https://api.openalex.org/works?per-page=50&filter=doi:" + urllib.parse.quote(q, safe=":/|"))
        except Exception as e:
            print("openalex", repr(e)[:80], file=sys.stderr)
            continue
        for w in res.get("results", []):
            inv = w.get("abstract_inverted_index") or {}
            words = sorted((pos, word) for word, ps in inv.items() for pos in ps)
            out["doi:" + (w.get("doi") or "").replace("https://doi.org/", "")] = " ".join(wd for _, wd in words) or None
        time.sleep(1)
    return {k.lower(): v for k, v in out.items()}


def fetch():
    rows, out = load_corpus(), {}
    path = os.path.join(CACHE, "abstracts.json")
    if os.path.exists(path):
        out = json.load(open(path))
    todo = [r for r in rows if not (out.get(r["id"]) or {}).get("abstract")]
    for i in range(0, len(todo), 100):
        chunk = todo[i:i + 100]
        for attempt in range(6):
            try:
                res = http("https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,abstract,venue,year",
                           json.dumps({"ids": [s2_id(r["id"]) for r in chunk]}).encode(), {"Content-Type": "application/json"})
                break
            except Exception as e:
                print("s2 retry", e, file=sys.stderr)
                time.sleep(30 * (attempt + 1))
        else:
            res = [None] * len(chunk)
        for r, d in zip(chunk, res):
            out[r["id"]] = {"abstract": (d or {}).get("abstract"), "venue": (d or {}).get("venue")}
        time.sleep(5)
    oa = openalex([r for r in rows if not out[r["id"]]["abstract"]])
    for r in rows:
        if not out[r["id"]]["abstract"] and oa.get(r["id"].lower()):
            out[r["id"]]["abstract"] = oa[r["id"].lower()]
    os.makedirs(CACHE, exist_ok=True)
    json.dump(out, open(path, "w"), indent=0)
    print("abstracts:", sum(bool(v["abstract"]) for v in out.values()), "of", len(out))


def parse(text):
    text = re.sub(r"<think>.*?</think>", "", text or "", flags=re.S)
    for m in re.finditer(r"\{[^{}]*\}", text):
        try:
            d = json.loads(m.group(0))
        except ValueError:
            continue
        if d.get("decision") in ("include", "exclude"):
            return {"decision": d["decision"], "category": str(d.get("category", "-"))[:1], "reason": str(d.get("reason", ""))[:160]}
    return None


def ask(model, record):
    body = {"model": model, "temperature": 0, "max_tokens": 1024, "messages": [
        {"role": "system", "content": CRITERIA},
        {"role": "user", "content": f"Title: {record['title']}\nYear: {record['year']}\nVenue: {record.get('venue') or '-'}\n"
                                    f"Abstract: {record.get('abstract') or '(not available: judge from title)'}"}]}
    for attempt in range(4):
        try:
            d = http(URL, json.dumps(body).encode(), {"Content-Type": "application/json",
                                                      "Authorization": f"Bearer {os.environ['MELIOUS_API_KEY']}"})
            u = d.get("usage") or {}
            p = parse(d["choices"][0]["message"].get("content"))
            if p:
                return dict(p, input_tokens=u.get("prompt_tokens", 0), output_tokens=u.get("completion_tokens", 0))
        except Exception as e:
            print(model, "retry", repr(e)[:80], file=sys.stderr)
        time.sleep(2 * (attempt + 1))
    return {"decision": "error", "category": "-", "reason": "no parseable answer", "input_tokens": 0, "output_tokens": 0}


def screen():
    abstracts = json.load(open(os.path.join(CACHE, "abstracts.json")))
    recs = [dict(r, **abstracts.get(r["id"], {})) for r in load_corpus()]
    for model in SCREENERS:
        path = os.path.join(CACHE, f"screen-{model}.json")
        done = json.load(open(path)) if os.path.exists(path) else {}
        todo = [r for r in recs if done.get(r["id"], {}).get("decision") not in ("include", "exclude")]
        with ThreadPoolExecutor(8) as ex:
            for r, res in zip(todo, ex.map(lambda r: ask(model, r), todo)):
                done[r["id"]] = res
        json.dump(done, open(path, "w"), indent=0)
        print(model, {k: sum(v["decision"] == k for v in done.values()) for k in ("include", "exclude", "error")})


def kappa(a, b):
    """Cohen's kappa for two equal-length label lists."""
    n = len(a)
    labels = set(a) | set(b)
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(l) / n) * (b.count(l) / n) for l in labels)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def load_screens():
    return [json.load(open(os.path.join(CACHE, f"screen-{m}.json"))) for m in SCREENERS]


def report():
    rows, (s1, s2) = load_corpus(), load_screens()
    abstracts = json.load(open(os.path.join(CACHE, "abstracts.json")))
    a = [s1[r["id"]]["decision"] for r in rows]
    b = [s2[r["id"]]["decision"] for r in rows]
    k = kappa(a, b)
    both = sum(x == y == "include" for x, y in zip(a, b))
    dis = [r for r, x, y in zip(rows, a, b) if x != y]
    cost = sum((s["input_tokens"] * p[0] + s["output_tokens"] * p[1]) / 1e6
               for s_, p in zip((s1, s2), ((0.10, 0.40), (0.15, 0.60))) for s in s_.values())
    lines = [f"# Screening of the §3.1 rerun set", "",
             f"- Records: {len(rows)}; abstracts retrieved: {sum(bool(abstracts.get(r['id'], {}).get('abstract')) for r in rows)}",
             f"- Screeners: {SCREENERS[0]} and {SCREENERS[1]} (Melious API, temperature 0, same criteria, blind to each other)",
             f"- Screener 1 includes: {a.count('include')}; screener 2 includes: {b.count('include')}; both include: {both}",
             f"- Raw agreement: {sum(x == y for x, y in zip(a, b)) / len(a):.3f}; Cohen's kappa: {k:.2f}",
             f"- Disagreements for adjudication: {len(dis)}", f"- LLM spend: €{cost:.4f}", "",
             "| id | title | S1 | S2 |", "|---|---|---|---|"]
    lines += [f"| {r['id']} | {r['title'][:90]} | {s1[r['id']]['decision']}: {s1[r['id']]['reason']} | "
              f"{s2[r['id']]['decision']}: {s2[r['id']]['reason']} |" for r in dis]
    open(os.path.join(ROOT, "docs", "screening.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines[:9]))


def apply():
    rows, (s1, s2) = load_corpus(), load_screens()
    adj_path = os.path.join(ROOT, "docs", "adjudication.csv")
    adj = {r["id"]: r for r in csv.DictReader(open(adj_path))} if os.path.exists(adj_path) else {}
    for r in rows:
        x, y = s1[r["id"]], s2[r["id"]]
        r["screener1"], r["screener2"] = x["decision"], y["decision"]
        if x["decision"] == y["decision"]:
            final, why, cat = x["decision"], "both screeners: " + x["reason"], x["category"]
        elif r["id"] in adj:
            final, why, cat = adj[r["id"]]["decision"], "adjudicated: " + adj[r["id"]]["reason"], adj[r["id"]].get("category", "-")
        else:
            final, why, cat = "unresolved", "screeners disagree; not adjudicated", "-"
        cited = re.match(r"include \(already cited", r["decision"])
        r["stage"] = "title/abstract"
        r["decision"] = final + (" (" + r["decision"].split("(", 1)[1] if cited and final == "include" else "")
        r["reason"] = why
        r["category"] = cat
    # taxonomy codes for includes: agreed code of both models, else docs/coding-adjudication.csv
    cpath, apath = os.path.join(CACHE, "coding.json"), os.path.join(ROOT, "docs", "coding-adjudication.csv")
    if os.path.exists(cpath):
        cj = json.load(open(cpath))
        cadj = {r["id"]: r["code"] for r in csv.DictReader(open(apath))} if os.path.exists(apath) else {}
        for r in rows:
            x, y = (cj[m].get(r["id"], {}).get("code") for m in SCREENERS)
            r["type"] = (x if x == y else cadj.get(r["id"], "unresolved")) if r["decision"].startswith("include") else ""
    cols = list(rows[0].keys())
    with open(CORPUS, "w", newline="") as f:
        w = csv.DictWriter(f, cols)
        w.writeheader()
        w.writerows(rows)
    c = lambda p: sum(r["decision"].startswith(p) for r in rows)
    print("include", c("include"), "exclude", c("exclude"), "unresolved", c("unresolved"))
    print("codes", {k: sum(r["type"] == k for r in rows) for k in list(CODES) + ["unresolved"]})


CODES = {"CAPTCHA": "a CAPTCHA/challenge (text, image, audio, puzzle, behavioral) or an attack/solver on one",
         "I": "Type I point-in-time JavaScript/VM challenge or proof-of-work run in the browser",
         "II": "Type II stateful telemetry: browser/device fingerprinting or long-term risk scoring for bot detection",
         "III": "Type III behavioral biometrics: mouse, keystroke, touch or sensor dynamics for bot detection",
         "IV": "Type IV anonymous attestation tokens (Privacy Pass, Private Access Tokens, PACT)",
         "V": "Type V hardware-anchored binding (device-bound sessions, WebAuthn/passkeys) used against automation",
         "ECON": "economics or ecosystem of bypass (solver farms, bot markets)",
         "OTHER": "none of the above"}
CODE_PROMPT = ("Classify this research record into exactly one class of a taxonomy of client-side anti-automation.\n"
               + "\n".join(f"{k}: {v}" for k, v in CODES.items())
               + '\nAnswer with exactly one JSON object and nothing else: {"code": "<class>", "reason": "<= 12 words"}')


def code():
    """Second-stage coding of included records into the paper's taxonomy, by both screener models (blind)."""
    abstracts = json.load(open(os.path.join(CACHE, "abstracts.json")))
    inc = [dict(r, **abstracts.get(r["id"], {})) for r in load_corpus() if r["decision"].startswith("include")]

    def one(model, r):
        body = {"model": model, "temperature": 0, "max_tokens": 512, "messages": [
            {"role": "system", "content": CODE_PROMPT},
            {"role": "user", "content": f"Title: {r['title']}\nAbstract: {r.get('abstract') or '(not available)'}"}]}
        for attempt in range(4):
            try:
                d = http(URL, json.dumps(body).encode(), {"Content-Type": "application/json",
                                                          "Authorization": f"Bearer {os.environ['MELIOUS_API_KEY']}"})
                t = re.sub(r"<think>.*?</think>", "", d["choices"][0]["message"].get("content") or "", flags=re.S)
                m = re.search(r"\{[^{}]*\}", t)
                c = json.loads(m.group(0)) if m else {}
                if c.get("code") in CODES:
                    u = d.get("usage") or {}
                    return {"code": c["code"], "reason": str(c.get("reason", ""))[:120],
                            "input_tokens": u.get("prompt_tokens", 0), "output_tokens": u.get("completion_tokens", 0)}
            except Exception as e:
                print(model, "retry", repr(e)[:80], file=sys.stderr)
            time.sleep(2 * (attempt + 1))
        return {"code": "ERROR", "reason": "", "input_tokens": 0, "output_tokens": 0}

    path = os.path.join(CACHE, "coding.json")
    out = json.load(open(path)) if os.path.exists(path) else {}
    for model in SCREENERS:
        done = out.setdefault(model, {})
        todo = [r for r in inc if done.get(r["id"], {}).get("code", "ERROR") == "ERROR"]
        with ThreadPoolExecutor(8) as ex:
            done.update(zip([r["id"] for r in todo], ex.map(lambda r: one(model, r), todo)))
    json.dump(out, open(path, "w"), indent=0)
    a, b = ([out[m][r["id"]]["code"] for r in inc] for m in SCREENERS)
    agree = [x for x, y in zip(a, b) if x == y]
    print(f"coded {len(inc)}; kappa {kappa(a, b):.2f}; agreed {len(agree)}")
    print("agreed codes:", {k: agree.count(k) for k in CODES})
    print("disagreements:", [(r["id"], x, y) for r, x, y in zip(inc, a, b) if x != y][:60])


def selfcheck():
    assert abs(kappa(["i", "i", "e", "e"], ["i", "e", "e", "e"]) - 0.5) < 1e-9
    assert kappa(["i", "e"], ["i", "e"]) == 1.0
    assert parse('<think>x</think> {"decision": "include", "category": "A", "reason": "VLM solver"}')["category"] == "A"
    assert parse("no json") is None
    assert s2_id("arXiv:2603.23559v2") == "ARXIV:2603.23559" and s2_id("doi:10.1/x") == "DOI:10.1/x"
    print("selfcheck ok")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "--selfcheck"
    {"fetch": fetch, "screen": screen, "report": report, "apply": apply, "code": code, "--selfcheck": selfcheck}[cmd]()
