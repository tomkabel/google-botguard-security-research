"""Config (d): hybrid (b)+(c). Scripted xdotool input for pages it recognises (window title
"Step N"); the VLM agent is invoked only for an unrecognised page (e.g. a CAPTCHA interstitial),
then scripted control resumes. Measures how much LLM spend the hybrid saves vs (c).
Env as in c_vlm.py. Usage: python d_hybrid.py [--runs N] [--start /flow/1]
"""
import argparse, os, re, shutil, time
from common import BASE, Run
from b_osinput import launch, window_title, drive_flow
from c_vlm import make_adapter, model_id, agent_loop, screen_size, SHOT_W, SHOT_H


def one_run(start, delay, max_steps):
    run = Run("d-hybrid", model=model_id())
    proc, prof = launch(f"{BASE}{start}{'&' if '?' in start else '?'}run={run.id}")
    try:
        time.sleep(3)
        run.act("launch")
        m = re.match(r"Step (\d)", window_title())
        if not m:  # unknown page: hand to the VLM until a known step appears
            w, h = screen_size()
            agent_loop(make_adapter(), run, "Complete the verification page shown in the browser, submit it, then click "
                       "'Continue to form' and stop once a page titled 'Step 1' is visible.",
                       max_steps, (w / SHOT_W, h / SHOT_H))
            m = re.match(r"Step (\d)", window_title())
        run.r["success"] = bool(m) and drive_flow(run, delay, int(m.group(1)))
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
    ap.add_argument("--start", default="/flow/1")
    ap.add_argument("--delay", type=float, default=0.08)
    ap.add_argument("--max-steps", type=int, default=20)
    a = ap.parse_args()
    for _ in range(a.runs):
        r = one_run(a.start, a.delay, a.max_steps)
        print(r["run_id"], "success" if r["success"] else f"fail {r['error']}")


if __name__ == "__main__":
    main()
