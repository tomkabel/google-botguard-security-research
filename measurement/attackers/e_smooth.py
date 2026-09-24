"""Experiment A: mouse-driven OS-level input on the base form, for kinematic scoring.

--path teleport : config b-mouse. Scripted xdotool as in (b), but clicks field and button: the pointer jumps
                  straight to each target (one motion event), as the VLM executor in (c) does.
--path minjerk  : config e-smooth. Same targets, reached along a minimum-jerk trajectory (Flash & Hogan 1985)
                  with a random lateral bow, Gaussian jitter, Fitts'-law duration and a short pause before the
                  click. Generic textbook parameters, fixed a priori; not tuned against any detector or vendor.
Targets are the base-form field/button centres in client pixels plus the viewport offset of Chromium on a
1280x800 Xvfb (VIEWPORT_OFFSET="0,121", measured 2026-09-24 via a click event).
Usage: DISPLAY=:99 RUN_LOG_DIR=../logs/kin python e_smooth.py --path minjerk --runs 10
"""
import argparse, math, os, random, shutil, subprocess, time
from common import BASE, FLOW, FLOW_ANSWERS, Run
from b_osinput import launch, xdo, wait_title

OFF = [int(v) for v in os.environ.get("VIEWPORT_OFFSET", "0,121").split(",")]
FIELD_X = {1: 115, 2: 84, 3: 72, 4: 128, 5: 190}  # left edge of #f<n> (158x21 at y=98), measured
BUTTON = (40, 200, 160, 40)


def minjerk(p0, p1, rng, hz=100):
    """Points and per-step sleep for a minimum-jerk move p0->p1 with lateral bow and jitter."""
    d = math.dist(p0, p1)
    T = (0.2 + 0.1 * math.log2(1 + d / 30)) * rng.uniform(0.85, 1.15)  # Fitts' law, a=0.2 s, b=0.1 s/bit
    n = max(2, int(T * hz))
    ux, uy = ((p1[0] - p0[0]) / d, (p1[1] - p0[1]) / d) if d else (0, 0)
    bow = rng.gauss(0, 0.06) * d  # peak lateral deviation, px
    pts = []
    for i in range(1, n + 1):
        tau = i / n
        s = 10 * tau ** 3 - 15 * tau ** 4 + 6 * tau ** 5
        lat = bow * math.sin(math.pi * s)
        jx, jy = (rng.gauss(0, 1.0), rng.gauss(0, 1.0)) if i < n else (0, 0)
        pts.append((round(p0[0] + s * (p1[0] - p0[0]) - uy * lat + jx), round(p0[1] + s * (p1[1] - p0[1]) + ux * lat + jy)))
    return pts, T / n


def pointer():
    out = subprocess.run(["xdotool", "getmouselocation", "--shell"], capture_output=True, text=True).stdout
    kv = dict(l.split("=") for l in out.split())
    return int(kv["X"]), int(kv["Y"])


def click_at(target, path, rng):
    if path == "teleport":
        xdo("mousemove", str(target[0]), str(target[1]))
    else:
        pts, dt = minjerk(pointer(), target, rng)
        cmd = []
        for x, y in pts:  # one xdotool process, so inter-sample timing is not dominated by process start
            cmd += ["mousemove", str(x), str(y), "sleep", f"{dt:.4f}"]
        xdo(*cmd)
        time.sleep(rng.uniform(0.08, 0.25))  # dwell before pressing
    xdo("click", "1")


def one_run(path, delay, rng):
    run = Run("b-mouse" if path == "teleport" else "e-smooth")
    proc, prof = launch(f"{BASE}{FLOW}/1?run={run.id}")
    try:
        run.act("launch")
        for i, ans in enumerate(FLOW_ANSWERS, 1):
            if not wait_title(f"Step {i}"):
                raise RuntimeError(f"step {i} not reached")
            fx = FIELD_X[i] + rng.uniform(40, 118) + OFF[0], 98 + rng.uniform(6, 15) + OFF[1]
            click_at((round(fx[0]), round(fx[1])), path, rng)
            run.act("click")
            xdo("type", "--delay", str(int(delay * 1000)), ans)
            run.act("type")
            bx = BUTTON[0] + rng.uniform(30, 130) + OFF[0], BUTTON[1] + rng.uniform(10, 30) + OFF[1]
            click_at((round(bx[0]), round(bx[1])), path, rng)
            run.act("click")
        run.r["success"] = wait_title("Done")
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
    ap.add_argument("--path", choices=["teleport", "minjerk"], default="minjerk")
    ap.add_argument("--delay", type=float, default=0.08, help="per-keystroke delay, s")
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    for _ in range(a.runs):
        r = one_run(a.path, a.delay, rng)
        print(r["run_id"], "success" if r["success"] else f"fail {r['error']}")


if __name__ == "__main__":
    main()
