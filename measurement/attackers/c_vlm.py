"""Config (c): VLM computer-use agent + OS-level input on stock Chrome (screenshot-only grounding).

Adapter interface (implement one per model/provider, e.g. an open model served locally):
    class Adapter:
        def step(self, screenshot_png: bytes, goal: str) -> tuple[list[dict], int, int]
            # returns (actions, input_tokens, output_tokens); action = {"action": name, **params}
            # an empty action list means the model considers the goal done.
Actions understood by the executor: screenshot, left_click{coordinate}, double_click{coordinate},
type{text}, key{text}, mouse_move{coordinate}, scroll{coordinate,...}, wait.

Concrete adapter: AnthropicAdapter (Claude computer use). Env:
  ANTHROPIC_MODEL (required, no default committed), ANTHROPIC_API_KEY or `ant auth login` profile,
  CU_TOOL = toolset (computer_toolset_20260801, GA; required on claude-opus-5-5)
          | legacy (computer_20251124 + beta computer-use-2025-11-24)
MeliousAdapter (VLM_PROVIDER=melious): OpenAI-compatible chat API at https://api.melious.ai/v1,
  MELIOUS_MODEL = exact model id, MELIOUS_API_KEY. One screenshot per call, strict JSON action out.
Usage: python c_vlm.py [--runs N] [--max-steps 40]
"""
import argparse, base64, json, os, re, shutil, subprocess, time
from common import BASE, Run
from b_osinput import launch, xdo, window_title

SHOT_W, SHOT_H = 1280, 800  # screenshots are downscaled to this; coordinates are scaled back
GOAL = ("Complete the web form shown in the browser: fill each step (name 'Test User', email "
        "'test@example.invalid', city 'Tartu', postal code '50090', confirmation 'YES') and press "
        "Continue until a 'Thank you' page appears. Then stop.")


def screen_size():
    out = subprocess.run(["xdotool", "getdisplaygeometry"], capture_output=True, text=True).stdout.split()
    return int(out[0]), int(out[1])


def screenshot():
    return subprocess.run(["import", "-window", "root", "-resize", f"{SHOT_W}x{SHOT_H}!", "png:-"],
                          capture_output=True, check=True).stdout


def execute(a, scale):
    """Run one action via xdotool. Returns True if the model should receive a fresh screenshot."""
    name = a.get("action")
    xy = a.get("coordinate")
    if xy:
        x, y = int(xy[0] * scale[0]), int(xy[1] * scale[1])
        xdo("mousemove", str(x), str(y))
    if name in ("left_click", "double_click"):
        xdo("click", *(["--repeat", "2"] if name == "double_click" else []), "1")
    elif name == "type":
        xdo("type", "--delay", "40", a.get("text", ""))
    elif name == "key":
        xdo("key", a.get("text", "").replace("Enter", "Return"))
    elif name == "scroll":
        xdo("click", "5" if a.get("scroll_direction", "down") == "down" else "4")
    elif name == "wait":
        time.sleep(1)
    return name in ("screenshot", "zoom")


class AnthropicAdapter:
    def __init__(self):
        import anthropic
        self.client = anthropic.Anthropic()
        self.model = os.environ["ANTHROPIC_MODEL"]
        self.toolset = os.environ.get("CU_TOOL", "toolset") == "toolset"
        self.messages = []

    def _img(self, png):
        return {"type": "image", "source": {"type": "base64", "media_type": "image/png",
                                            "data": base64.b64encode(png).decode()}}

    def step(self, png, goal):
        if not self.messages:
            self.messages.append({"role": "user", "content": [{"type": "text", "text": goal}, self._img(png)]})
        if self.toolset:
            resp = self.client.messages.create(model=self.model, max_tokens=4096, messages=self.messages,
                                               tools=[{"type": "computer_toolset_20260801"}])
        else:
            resp = self.client.beta.messages.create(
                model=self.model, max_tokens=4096, messages=self.messages, betas=["computer-use-2025-11-24"],
                tools=[{"type": "computer_20251124", "name": "computer",
                        "display_width_px": SHOT_W, "display_height_px": SHOT_H}])
        self.messages.append({"role": "assistant", "content": [b.model_dump(exclude_none=True) for b in resp.content]})
        uses = [b for b in resp.content if b.type == "tool_use"]
        self._pending = uses
        actions = [dict(b.input, action=b.input.get("action", b.name)) for b in uses]
        return actions, resp.usage.input_tokens, resp.usage.output_tokens

    def results(self, png):
        """Answer every pending tool_use in one user message (latest screenshot attached to each)."""
        content = []
        for b in self._pending:
            r = {"type": "tool_result", "tool_use_id": b.id, "content": [self._img(png)]}
            if self.toolset:
                r["toolset_name"] = "computer"
            content.append(r)
        self.messages.append({"role": "user", "content": content})


ACTION_PROMPT = ("You control a web browser through the screenshot below ({w}x{h} pixels, origin top-left).\n"
                 "Task: {goal}\nActions already taken (oldest first): {hist}\n"
                 "Reply with exactly ONE JSON object and nothing else, one of:\n"
                 '{{"action":"click","x":<int>,"y":<int>}}  {{"action":"type","text":"<str>"}}  '
                 '{{"action":"key","key":"Enter"}}  {{"action":"done"}}\n'
                 "x,y are pixel coordinates in this screenshot. Click a field before typing into it.")


def parse_action(text):
    """Model reply -> executor action list ([] = done, None = unparseable). Tolerates fences/prose."""
    text = re.sub(r"<think>.*?</think>", "", text or "", flags=re.S)
    for m in re.finditer(r"\{[^{}]*\}", text):
        try:
            a = json.loads(m.group(0))
        except ValueError:
            continue
        kind = str(a.get("action", "")).lower()
        if kind == "done":
            return []
        if kind == "click":
            xy = a.get("coordinate") or [a.get("x"), a.get("y")]
            if all(isinstance(v, (int, float)) for v in xy[:2]):
                return [{"action": "left_click", "coordinate": [round(xy[0]), round(xy[1])]}]
        if kind == "type" and isinstance(a.get("text"), str):
            return [{"action": "type", "text": a["text"]}]
        if kind == "key":
            return [{"action": "key", "text": str(a.get("key") or a.get("text") or "Return")}]
    return None


class MeliousAdapter:
    """Stateless per call: goal + text history of own actions + current screenshot."""
    URL = "https://api.melious.ai/v1/chat/completions"

    def __init__(self, model=None):
        import httpx
        self.http = httpx.Client(timeout=120)
        self.model = model or os.environ["MELIOUS_MODEL"]
        self.hist, self.calls = [], []

    def ask(self, png, prompt, max_tokens=2048):
        """One chat call; returns (reply text, input tokens, output tokens, latency s)."""
        import httpx
        body = {"model": self.model, "temperature": 0, "max_tokens": max_tokens, "messages": [{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": "data:image/png;base64," + base64.b64encode(png).decode()}},
            {"type": "text", "text": prompt}]}]}
        # retry transport errors and non-200s (Melious intermittently answers image requests with 400
        # "malformed" for requests that succeed on resend); failed attempts are logged, latency = successful call
        for attempt in range(3):
            t = time.monotonic()
            try:
                r = self.http.post(self.URL, headers={"Authorization": f"Bearer {os.environ['MELIOUS_API_KEY']}"}, json=body)
            except httpx.TransportError as e:
                self.calls.append({"error": repr(e)[:120]})
                continue
            dt = time.monotonic() - t
            if r.status_code == 200:
                break
            self.calls.append({"error": f"HTTP {r.status_code}: {r.text[:80]}"})
        else:
            raise RuntimeError("melious: 3 failed attempts")
        d = r.json()
        u = d.get("usage") or {}
        i, o = u.get("prompt_tokens", 0), u.get("completion_tokens", 0)
        self.calls.append({"latency_s": dt, "input_tokens": i, "output_tokens": o})
        return d["choices"][0]["message"].get("content") or "", i, o, dt

    def step(self, png, goal):
        text, i, o, _ = self.ask(png, ACTION_PROMPT.format(w=SHOT_W, h=SHOT_H, goal=goal,
                                                           hist=json.dumps(self.hist[-12:]) or "none"))
        acts = parse_action(text)
        if acts is None:  # unparseable reply: log it and let the loop re-ask with a fresh screenshot
            self.hist.append({"invalid_reply": text[:80]})
            return [{"action": "screenshot"}], i, o
        self.hist += acts
        return acts, i, o

    def results(self, png):
        pass  # stateless: the next step() carries the new screenshot


def make_adapter():
    return MeliousAdapter() if os.environ.get("VLM_PROVIDER") == "melious" else AnthropicAdapter()


def model_id():
    return os.environ.get("MELIOUS_MODEL") if os.environ.get("VLM_PROVIDER") == "melious" else os.environ.get("ANTHROPIC_MODEL")


def agent_loop(adapter, run, goal, max_steps, scale):
    run.r["llm_calls"] = getattr(adapter, "calls", [])  # same list object: survives exceptions
    png = screenshot()
    for _ in range(max_steps):
        actions, i, o = adapter.step(png, goal)
        run.tokens(i, o)
        run.act("llm")
        if not actions:
            break
        for a in actions:
            execute(a, scale)
            run.act(a["action"])
        time.sleep(0.5)
        png = screenshot()
        adapter.results(png)


def one_run(max_steps):
    run = Run("c-vlm", model=model_id())
    proc, prof = launch(f"{BASE}/flow/1?run={run.id}")
    try:
        time.sleep(3)
        run.act("launch")
        w, h = screen_size()
        agent_loop(make_adapter(), run, GOAL, max_steps, (w / SHOT_W, h / SHOT_H))
        # success is decided server-side (flow_done event) in analyze.py; window title is a hint
        run.r["success"] = window_title().startswith("Done")
    except Exception as e:
        run.r["error"] = repr(e)
    finally:
        proc.terminate()
        proc.wait(timeout=10)
        shutil.rmtree(prof, ignore_errors=True)
    return run.save()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--max-steps", type=int, default=40)
    a = ap.parse_args()
    for _ in range(a.runs):
        r = one_run(a.max_steps)
        print(r["run_id"], "success" if r["success"] else f"fail {r['error']}",
              r["input_tokens"], r["output_tokens"])


def selfcheck():
    assert parse_action('```json\n{"action":"click","x":120.4,"y":220}\n```') == [{"action": "left_click", "coordinate": [120, 220]}]
    assert parse_action('<think>{"action":"done"}</think> ok {"action": "type", "text": "Tartu"}') == [{"action": "type", "text": "Tartu"}]
    assert parse_action('{"action":"key","key":"Enter"}') == [{"action": "key", "text": "Enter"}]
    assert parse_action('I am done. {"action":"done"}') == [] and parse_action("no json") is None
    print("selfcheck ok")


if __name__ == "__main__":
    import sys
    if "--selfcheck" in sys.argv:
        raise SystemExit(selfcheck())
    main()
