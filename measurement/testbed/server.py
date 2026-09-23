"""Self-hosted anti-automation testbed (stdlib only). Binds to 127.0.0.1 only.

Pages (append ?run=<run_id> so server events join attacker runs):
  /flow/1 .. /flow/5   five-step form, each step carries the cognitive-honeypot decoy (paper §3.4 L3)
  /flow/done           end of flow
  /turnstile?mode=pass|fail   Cloudflare Turnstile with documented TEST site keys
  /recaptcha                  reCAPTCHA v2 documented TEST key (Google publishes no v3 test key;
                              set RECAPTCHA_V3_SITEKEY/SECRET to a key you registered for localhost)
Endpoints:
  POST /event   client-side telemetry (clicks, timings, honeypot)
  POST /verify  token verification; calls vendor siteverify with TEST secrets only when --verify is set

Every event is appended to logs/server.jsonl.
"""
import argparse, html, json, os, sys, threading, time, urllib.parse, urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

LOG = os.path.join(os.path.dirname(__file__), "..", "logs", "server.jsonl")
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


def log(ev):
    ev["server_ts"] = time.time()
    with _lock, open(LOG, "a") as f:
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
</script>"""

# Paper §3.4 L3, implemented as specified: decoy with non-zero getBoundingClientRect(), plausible
# text/attributes, opacity 0.01, inside a full-viewport overlay with pointer-events:none so human
# (coordinate) clicks pass through to the real button beneath; aria-hidden + tabindex=-1 so
# screen-reader/keyboard users never reach it. Only selection by element reference (JS/CDP
# el.click(), dispatchEvent) fires its handler.
DECOY = """<div id="hp-overlay" aria-hidden="true" style="position:fixed;inset:0;pointer-events:none;z-index:10">
  <button id="hp-decoy" type="button" tabindex="-1" name="continue" class="btn-primary"
    style="position:absolute;left:40px;top:{top}px;width:160px;height:40px;opacity:0.01"
    onclick="send('honeypot',{{trusted:event.isTrusted}});this.dataset.hit=1">Continue</button>
</div>"""


def page(title, body, decoy_top=None):
    decoy = DECOY.format(top=decoy_top) if decoy_top is not None else ""
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
                            ["/flow/1", "/turnstile?mode=pass", "/turnstile?mode=fail", "/recaptcha", "/recaptcha3"])
            return self._send(200, page("Testbed", f"<ul>{links}</ul>"))
        self._send(404, "not found", "text/plain")

    def do_POST(self):
        raw = self.rfile.read(int(self.headers.get("Content-Length", 0) or 0))[:65536].decode(errors="replace")
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
