"""Config (b): scripted OS-level input (xdotool) on a stock, non-automated Chrome/Chromium.

No CDP, no webdriver flag: the browser is launched normally with a throwaway profile and driven
only through X11 synthetic keyboard input. Keyboard path: type field, Return submits the form
(the decoy is out of tab order, so it is never focused).
Requires: X11 session, xdotool, a Chrome/Chromium binary (CHROME env, default chromium).
Usage: python b_osinput.py [--runs N] [--delay 0.08]
"""
import argparse, os, shutil, subprocess, tempfile, time
from common import BASE, FLOW_ANSWERS, Run

CHROME = os.environ.get("CHROME", "chromium")


# Display safety: (b)-(d) inject OS-level input. Refuse the live desktop unless explicitly allowed;
# run under Xvfb, e.g. `Xvfb :99 -screen 0 1280x800x24 & DISPLAY=:99 python b_osinput.py`.
def xdo(*args):
    assert os.environ.get("DISPLAY") not in (None, "", ":0", ":0.0") or os.environ.get("ALLOW_LIVE_DISPLAY") == "1", \
        "refusing to inject input into the live display; set DISPLAY to an Xvfb server"
    subprocess.run(["xdotool", *args], check=True)


def window_title():
    return subprocess.run(["xdotool", "getwindowfocus", "getwindowname"],  # works without an EWMH WM (Xvfb)
                          capture_output=True, text=True).stdout.strip()


def launch(url):
    prof = tempfile.mkdtemp(prefix="tb-chrome-")
    proc = subprocess.Popen([CHROME, f"--user-data-dir={prof}", "--no-first-run",
                             "--no-default-browser-check", "--window-position=0,0",
                             "--window-size=1280,800", "--new-window", url],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return proc, prof


def wait_title(prefix, timeout=15):
    end = time.time() + timeout
    while time.time() < end:
        if window_title().startswith(prefix):
            return True
        time.sleep(0.2)
    return False


def drive_flow(run, delay, start_step=1):
    """Keyboard-only flow; returns True when the Done page is reached."""
    for i in range(start_step, 6):
        if not wait_title(f"Step {i}"):
            return False
        xdo("type", "--delay", str(int(delay * 1000)), FLOW_ANSWERS[i - 1])
        run.act("type")
        xdo("key", "Return")
        run.act("key")
    return wait_title("Done")


def one_run(delay):
    run = Run("b-xdotool")
    proc, prof = launch(f"{BASE}/flow/1?run={run.id}")
    try:
        run.act("launch")
        run.r["success"] = drive_flow(run, delay)
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
    ap.add_argument("--delay", type=float, default=0.08, help="per-keystroke delay, s")
    a = ap.parse_args()
    for _ in range(a.runs):
        r = one_run(a.delay)
        print(r["run_id"], "success" if r["success"] else f"fail {r['error']}")


if __name__ == "__main__":
    main()
