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
Usage: python c_vlm.py [--runs N] [--max-steps 40]
"""
import argparse, base64, os, shutil, subprocess, time
from common import BASE, Run
from b_osinput import launch, xdo

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


def agent_loop(adapter, run, goal, max_steps, scale):
    png = screenshot()
    for _ in range(max_steps):
        actions, i, o = adapter.step(png, goal)
        run.tokens(i, o)
        run.act("llm")
        if not actions:
            return
        for a in actions:
            execute(a, scale)
            run.act(a["action"])
        time.sleep(0.5)
        png = screenshot()
        adapter.results(png)


def one_run(max_steps):
    run = Run("c-vlm", model=os.environ.get("ANTHROPIC_MODEL"))
    proc, prof = launch(f"{BASE}/flow/1?run={run.id}")
    try:
        time.sleep(3)
        run.act("launch")
        w, h = screen_size()
        agent_loop(AnthropicAdapter(), run, GOAL, max_steps, (w / SHOT_W, h / SHOT_H))
        # success is decided server-side (flow_done event) in analyze.py; window title is a hint
        run.r["success"] = subprocess.run(["xdotool", "getactivewindow", "getwindowname"],
                                          capture_output=True, text=True).stdout.startswith("Done")
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


if __name__ == "__main__":
    main()
