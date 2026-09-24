"""Self-hosted anti-automation testbed (stdlib only). Binds to 127.0.0.1 only.

Pages (append ?run=<run_id> so server events join attacker runs):
  /flow/1 .. /flow/5   five-step form, each step carries the cognitive-honeypot decoy (paper §3.4 L3)
  /flow/done           end of flow
  /v/<k>/flow/1 .. 5   Experiment B: unseen variant k (1-9) of the five-step form, same answers, honeypot on
                       every page; step_submit events carry variant + ok (answer correct), then flow_done
  /turnstile?mode=pass|fail   Cloudflare Turnstile with documented TEST site keys
  /recaptcha                  reCAPTCHA v2 documented TEST key (Google publishes no v3 test key;
                              set RECAPTCHA_V3_SITEKEY/SECRET to a key you registered for localhost)
Endpoints:
  POST /event   client-side telemetry (clicks, timings, honeypot)
  POST /verify  token verification; calls vendor siteverify with TEST secrets only when --verify is set
  POST /kin     pointer kinematics (mousemove/mousedown/click/keydown, performance.now() + client x/y)

Every event is appended to logs/server.jsonl; kinematics go to logs/kinematics.jsonl.
"""
import argparse, html, json, os, random, sys, threading, time, urllib.parse, urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

LOG = os.path.join(os.path.dirname(__file__), "..", "logs", "server.jsonl")
KIN_LOG = os.path.join(os.path.dirname(__file__), "..", "logs", "kinematics.jsonl")
_lock = threading.Lock()
VERIFY_ONLINE = False

# Documented vendor TEST keys (verified 2026-09-23):
# https://developers.cloudflare.com/turnstile/troubleshooting/testing/
TURNSTILE = {"pass": ("1x00000000000000000000AA", "1x0000000000000000000000000000000AA"),
             "fail": ("2x00000000000000000000AB", "2x0000000000000000000000000000000AA")}
# https://developers.google.com/recaptcha/docs/faq  ("For reCAPTCHA v2, use the following test keys")
RECAPTCHA_V2 = ("6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI", "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe")
RECAPTCHA_V3 = (os.environ.get("RECAPTCHA_V3_SITEKEY"), os.environ.get("RECAPTCHA_V3_SECRET"))
SITEVERIFY = {"turnstile": "https://challenges.cloudflare.com/turnstile/v0/siteverify",
              "recaptcha": "https://www.google.com/recaptcha/api/siteverify"}


def log(ev, path=LOG):
    ev["server_ts"] = time.time()
    with _lock, open(path, "a") as f:
        f.write(json.dumps(ev) + "\n")


# Client telemetry: page-load time, every click (trusted flag + coordinates + target), honeypot.
TELEMETRY = """<script>
const RUN = new URLSearchParams(location.search).get('run') || 'anon';
const T0 = performance.now();
function send(kind, extra) {
  const body = JSON.stringify(Object.assign({run: RUN, page: location.pathname, kind,
    t_ms: performance.now() - T0, webdriver: navigator.webdriver === true}, extra || {}));
  navigator.sendBeacon ? navigator.sendBeacon('/event', body) : fetch('/event', {method: 'POST', body});
}
send('load');
document.addEventListener('click', e => send('click', {target: e.target.id || e.target.tagName,
  trusted: e.isTrusted, x: e.clientX, y: e.clientY}), true);
// Pointer kinematics (Experiment A): [type, t_ms, clientX, clientY]; m=mousemove d=mousedown c=click k=keydown.
// Key identity is not recorded. Flushed on submit, on pagehide, and every 1500 events (sendBeacon 64 KB cap).
const KIN = [];
function flushKin() {
  if (KIN.length) navigator.sendBeacon('/kin', JSON.stringify({run: RUN, page: location.pathname, ev: KIN.splice(0)}));
}
function kin(k, e) {
  KIN.push([k, Math.round((performance.now() - T0) * 10) / 10, e.clientX | 0, e.clientY | 0]);
  if (KIN.length >= 1500) flushKin();
}
[['mousemove', 'm'], ['mousedown', 'd'], ['click', 'c'], ['keydown', 'k']].forEach(
  ([type, k]) => document.addEventListener(type, e => kin(k, e), true));
document.addEventListener('submit', flushKin, true);
addEventListener('pagehide', flushKin);
</script>"""

# Paper §3.4 L3, implemented as specified: decoy with non-zero getBoundingClientRect(), plausible
# text/attributes, opacity 0.01, inside a full-viewport overlay with pointer-events:none so human
# (coordinate) clicks pass through to the real button beneath; aria-hidden + tabindex=-1 so
# screen-reader/keyboard users never reach it. Only selection by element reference (JS/CDP
# el.click(), dispatchEvent) fires its handler.
DECOY = """<div id="hp-overlay" aria-hidden="true" style="position:fixed;inset:0;pointer-events:none;z-index:10">
  <button id="hp-decoy" type="button" tabindex="-1" name="continue" class="btn-primary"
    style="position:absolute;left:40px;top:{top}px;width:160px;height:40px;opacity:0.01"
    onclick="send('honeypot',{{trusted:event.isTrusted}});this.dataset.hit=1">{text}</button>
</div>"""


def page(title, body, decoy_top=None, decoy_text="Continue"):
    decoy = DECOY.format(top=decoy_top, text=html.escape(decoy_text)) if decoy_top is not None else ""
    return (f"<!doctype html><html><head><meta charset=utf-8><title>{html.escape(title)}</title>"
            f"{TELEMETRY}</head><body style='font:16px sans-serif;margin:40px'>{body}{decoy}</body></html>")


FIELDS = {1: ("name", "Full name"), 2: ("email", "Email"), 3: ("city", "City"),
          4: ("zip", "Postal code"), 5: ("agree", "Type YES to confirm")}


def flow_step(n, run):
    fname, label = FIELDS[n]
    nxt = f"/flow/{n + 1}" if n < 5 else "/flow/done"
    # Real button sits at the same position as the decoy, so a coordinate click lands on the real one.
    body = (f"<h1>Step {n} of 5</h1><form method=get action='{nxt}'>"
            f"<input type=hidden name=run value='{html.escape(run)}'>"
            f"<label>{label} <input id=f{n} name={fname} required autofocus></label>"
            f"<div style='position:absolute;left:40px;top:200px'>"
            f"<button id=real-continue type=submit style='width:160px;height:40px'>Continue</button></div></form>")
    return page(f"Step {n}", body, decoy_top=200)


# Experiment B: unseen variants of the five-step form at /v/<k>/flow/1..5. Same five answers as the base
# form; the honeypot decoy (same text as the real button) sits over the real button on every page.
STEPS = [["name"], ["email"], ["city"], ["zip"], ["agree"]]
EXPECTED = {"name": "test user", "first": "test", "last": "user", "email": "test@example.invalid",
            "email2": "test@example.invalid", "city": "tartu", "zip": "50090", "agree": "yes"}
LABELS = {
    "en": {"name": "Full name", "first": "First name", "last": "Last name", "email": "Email",
           "email2": "Repeat email", "city": "City", "zip": "Postal code", "agree": "Type YES to confirm",
           "agree_box": "I confirm these details", "company": "Company (optional)"},
    "de": {"name": "Vollständiger Name", "first": "Vorname", "last": "Nachname", "email": "E-Mail",
           "email2": "E-Mail wiederholen", "city": "Stadt", "zip": "Postleitzahl",
           "agree": "Zur Bestätigung YES eingeben", "agree_box": "Ich bestätige die Angaben",
           "company": "Firma (optional)"},
}
CITIES = ["Tallinn", "Tartu", "Pärnu", "Narva", "Viljandi"]
VARIANTS = {
    1: {"desc": "reworded labels", "labels": {"name": "Your name", "email": "E-mail address", "city": "Town",
                                              "zip": "ZIP code", "agree": "Enter YES to agree"}},
    2: {"desc": "German labels/title, button 'Weiter'", "lang": "de", "button": "Weiter"},
    3: {"desc": "randomised ids/names", "random_ids": True},
    4: {"desc": "optional decoy field placed first", "decoy_field": True},
    5: {"desc": "two fields per page, reordered", "steps": [["last", "first"], ["email", "email2"], ["city"], ["zip"], ["agree"]]},
    6: {"desc": "icon button placed above the field", "button": "→", "button_above": True},
    7: {"desc": "dropdown for city", "city_select": True},
    8: {"desc": "checkbox for confirmation", "agree_checkbox": True},
    9: {"desc": "combined: German, random ids, decoy field, button above, dropdown, checkbox", "lang": "de",
        "button": "Weiter", "random_ids": True, "decoy_field": True, "button_above": True, "city_select": True,
        "agree_checkbox": True},
}


def variant_fields(k, n):
    """Deterministic field list for variant k, step n: dicts with key, id, name, label, kind."""
    v = VARIANTS[k]
    labels = dict(LABELS[v.get("lang", "en")], **v.get("labels", {}))
    keys = (["company"] if v.get("decoy_field") else []) + v.get("steps", STEPS)[n - 1]
    rnd = random.Random(f"variant-{k}-{n}")
    out = []
    for i, key in enumerate(keys):
        kind = ("select" if key == "city" and v.get("city_select") else
                "checkbox" if key == "agree" and v.get("agree_checkbox") else "text")
        if v.get("random_ids"):
            fid, name = (f"{c}{rnd.getrandbits(40):010x}" for c in "xq")
        else:
            main = i == (1 if v.get("decoy_field") else 0)
            fid, name = (f"f{n}" if main else f"f{n}{key}"), key
        label = labels["agree_box"] if kind == "checkbox" else labels[key]
        out.append({"key": key, "id": fid, "name": name, "label": label, "kind": kind})
    return out


def variant_step(k, n, run):
    v = VARIANTS[k]
    de = v.get("lang") == "de"
    fields = variant_fields(k, n)
    nxt = f"/v/{k}/flow/{n + 1}" if n < 5 else f"/v/{k}/flow/done"
    rows = []
    for i, f in enumerate(fields):
        req = "" if f["key"] == "company" else " required"
        af = " autofocus" if i == 0 else ""
        attrs = f"id={f['id']} name={f['name']}{req}{af}"
        if f["kind"] == "select":
            opts = "".join(f"<option>{c}</option>" for c in CITIES)
            ctl = f"{html.escape(f['label'])} <select {attrs}><option value=''>–</option>{opts}</select>"
        elif f["kind"] == "checkbox":
            ctl = f"<input type=checkbox value=YES {attrs}> {html.escape(f['label'])}"
        else:
            ctl = f"{html.escape(f['label'])} <input {attrs}>"
        rows.append(f"<div style='margin:8px 0'><label>{ctl}</label></div>")
    top = 130 if v.get("button_above") else 170 + 45 * len(fields)
    text = v.get("button", "Continue")
    aria = " aria-label='Next'" if text == "→" else ""
    body = (f"<h1>{'Schritt' if de else 'Step'} {n} {'von' if de else 'of'} 5</h1><form method=get action='{nxt}'>"
            f"<input type=hidden name=run value='{html.escape(run)}'>"
            f"<div style='margin-top:{70 if v.get('button_above') else 0}px'>{''.join(rows)}</div>"
            f"<div style='position:absolute;left:40px;top:{top}px'>"
            f"<button id=real-continue type=submit{aria} style='width:160px;height:40px'>{html.escape(text)}</button>"
            f"</div></form>")
    return page(f"{'Schritt' if de else 'Step'} {n}", body, decoy_top=top, decoy_text=text)


def variant_ok(k, n, q):
    """True if every required field of step n was submitted with the expected answer."""
    norm = lambda s: " ".join(s.split()).lower()
    return all(norm(q.get(f["name"], "")) == EXPECTED[f["key"]] for f in variant_fields(k, n) if f["key"] != "company")


def captcha_page(vendor, sitekey, run, mode=""):
    if vendor == "turnstile":
        widget = (f"<script src='https://challenges.cloudflare.com/turnstile/v0/api.js' async defer></script>"
                  f"<div class='cf-turnstile' data-sitekey='{sitekey}'></div>")
        field = "cf-turnstile-response"
    elif vendor == "recaptcha_v3":
        widget = (f"<script src='https://www.google.com/recaptcha/api.js?render={sitekey}'></script>"
                  f"<script>grecaptcha.ready(()=>grecaptcha.execute('{sitekey}',{{action:'submit'}})"
                  f".then(t=>document.getElementById('tok').value=t))</script><input type=hidden id=tok name=token>")
        field = "token"
    else:
        widget = (f"<script src='https://www.google.com/recaptcha/api.js' async defer></script>"
                  f"<div class='g-recaptcha' data-sitekey='{sitekey}'></div>")
        field = "g-recaptcha-response"
    body = (f"<h1>Verify ({vendor} {mode})</h1><form method=post action='/verify'>"
            f"<input type=hidden name=run value='{html.escape(run)}'><input type=hidden name=vendor value='{vendor}'>"
            f"<input type=hidden name=mode value='{mode}'><input type=hidden name=field value='{field}'>"
            f"{widget}<button id=submit type=submit>Submit</button></form>")
    return page(f"Verify {vendor}", body)


def verify(vendor, mode, token):
    if vendor == "turnstile":
        secret = TURNSTILE.get(mode, TURNSTILE["pass"])[1]
    elif vendor == "recaptcha_v3":
        secret = RECAPTCHA_V3[1]
    else:
        secret = RECAPTCHA_V2[1]
    if not VERIFY_ONLINE or not secret:
        return {"verified": None, "note": "offline (start server with --verify)"}
    url = SITEVERIFY["turnstile" if vendor == "turnstile" else "recaptcha"]
    data = urllib.parse.urlencode({"secret": secret, "response": token}).encode()
    try:
        with urllib.request.urlopen(url, data, timeout=10) as r:
            res = json.load(r)
        return {"verified": bool(res.get("success")), "score": res.get("score"), "raw": res}
    except OSError as e:
        return {"verified": None, "error": str(e)}


class H(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="text/html"):
        b = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        q = dict(urllib.parse.parse_qsl(u.query))
        run = q.get("run", "anon")
        p = u.path.rstrip("/")
        if p.startswith("/flow/") and p[6:].isdigit() and 1 <= int(p[6:]) <= 5:
            n = int(p[6:])
            if n > 1:  # the submitted field of the previous step
                log({"run": run, "kind": "step_submit", "step": n - 1, "field_len": len(q.get(FIELDS[n - 1][0], ""))})
            return self._send(200, flow_step(n, run))
        if p == "/flow/done":
            log({"run": run, "kind": "step_submit", "step": 5, "field_len": len(q.get("agree", ""))})
            log({"run": run, "kind": "flow_done"})
            return self._send(200, page("Done", "<h1 id=done>Thank you</h1>"))
        parts = p.split("/")  # /v/<k>/flow/<n|done>
        if len(parts) == 5 and parts[1] == "v" and parts[3] == "flow" and parts[2].isdigit() and int(parts[2]) in VARIANTS:
            k, s = int(parts[2]), parts[4]
            n = 6 if s == "done" else int(s) if s.isdigit() and 1 <= int(s) <= 5 else None
            if n is None:
                return self._send(404, "not found", "text/plain")
            if n > 1:
                log({"run": run, "kind": "step_submit", "variant": k, "step": n - 1, "ok": variant_ok(k, n - 1, q)})
            if n <= 5:
                return self._send(200, variant_step(k, n, run))
            log({"run": run, "kind": "flow_done", "variant": k})
            de = VARIANTS[k].get("lang") == "de"
            return self._send(200, page("Fertig" if de else "Done", f"<h1 id=done>{'Vielen Dank' if de else 'Thank you'}</h1>"))
        if p == "/turnstile":
            mode = q.get("mode", "pass")
            return self._send(200, captcha_page("turnstile", TURNSTILE.get(mode, TURNSTILE["pass"])[0], run, mode))
        if p == "/recaptcha":
            return self._send(200, captcha_page("recaptcha_v2", RECAPTCHA_V2[0], run))
        if p == "/recaptcha3":
            if not RECAPTCHA_V3[0]:
                return self._send(404, page("n/a", "<p>Set RECAPTCHA_V3_SITEKEY (no official v3 test key exists).</p>"))
            return self._send(200, captcha_page("recaptcha_v3", RECAPTCHA_V3[0], run))
        if p == "":
            links = "".join(f"<li><a href='{h}'>{h}</a></li>" for h in
                            ["/flow/1", "/turnstile?mode=pass", "/turnstile?mode=fail", "/recaptcha", "/recaptcha3"]
                            + [f"/v/{k}/flow/1" for k in VARIANTS])
            return self._send(200, page("Testbed", f"<ul>{links}</ul>"))
        self._send(404, "not found", "text/plain")

    def do_POST(self):
        size = min(int(self.headers.get("Content-Length", 0) or 0), 1 << 20)
        if self.path == "/kin":
            try:
                ev = json.loads(self.rfile.read(size))
                ev = {"run": str(ev["run"])[:64], "page": str(ev["page"])[:64],
                      "ev": [[str(e[0])[:1], float(e[1]), int(e[2]), int(e[3])] for e in ev["ev"][:5000]]}
            except (ValueError, KeyError, TypeError, IndexError):
                return self._send(400, "bad kinematics", "text/plain")
            log(ev, KIN_LOG)
            return self._send(204, "")
        raw = self.rfile.read(size)[:65536].decode(errors="replace")
        if self.path == "/event":
            try:
                ev = json.loads(raw)
                assert isinstance(ev, dict)
            except (ValueError, AssertionError):
                return self._send(400, "bad json", "text/plain")
            ev = {k: ev[k] for k in list(ev)[:20]}  # bound untrusted input
            log(ev)
            return self._send(204, "")
        if self.path == "/verify":
            f = dict(urllib.parse.parse_qsl(raw))
            vendor, mode = f.get("vendor", ""), f.get("mode", "")
            token = f.get(f.get("field", ""), "")
            res = verify(vendor, mode, token)
            log({"run": f.get("run", "anon"), "kind": "verify", "vendor": vendor, "mode": mode,
                 "token_present": bool(token), **{k: v for k, v in res.items() if k != "raw"}})
            ok = res.get("verified")
            return self._send(200, page("Result", f"<h1 id=result>{'PASS' if ok else 'FAIL' if ok is False else 'UNVERIFIED'}</h1>"
                                        f"<a id=next href='/flow/1?run={html.escape(f.get('run', 'anon'))}'>Continue to form</a>"))
        self._send(404, "not found", "text/plain")

    def log_message(self, *a):
        pass


def main():
    global VERIFY_ONLINE
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8799)
    ap.add_argument("--verify", action="store_true", help="call vendor siteverify with TEST secrets")
    a = ap.parse_args()
    VERIFY_ONLINE = a.verify
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    print(f"testbed on http://127.0.0.1:{a.port}  log={os.path.abspath(LOG)}", file=sys.stderr)
    HTTPServer(("127.0.0.1", a.port), H).serve_forever()


if __name__ == "__main__":
    main()
