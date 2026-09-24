"""Experiment A: a kinematic (Type III / L1b) detector for point-to-click mouse movements.

Human class: Balabit Mouse Dynamics Challenge training sessions (github.com/balabit/Mouse-Dynamics-Challenge,
clone into measurement/data/). Bot class: synthetic straight-line / teleport movements generated from the
same human endpoints. Agents are scored from logs/kinematics.jsonl (browser mousemove/mousedown events).

Domain shift handling: Balabit is remote-desktop data (client timestamps, ~60 Hz); browser events arrive at
the input rate. Both are resampled by linear interpolation onto one 50 Hz grid before any feature is computed,
so sample count measures duration on a common clock rather than device event rate. Pixels are not rescaled.

Classifier: scikit-learn is not installed, so a transparent threshold rule
    bot  iff  samples < N  or  straightness > S
with (N, S) chosen by grid search on training users, reported on held-out users.
"""
import csv, glob, math, os, random
import numpy as np

RATE = 50.0   # Hz, common resampling grid
GAP = 1.0     # s; a pause longer than this between moves starts a new movement
MIN_TRAVEL = 20  # px; human reference keeps point-and-click movements only
TEST_USERS = {"user12", "user20", "user29", "user9"}  # held out; the other six users train
FEATURES = ["samples", "duration_s", "straightness", "v_mean", "v_std", "a_std", "jerk_mean", "curvature", "pause_s"]


def segments(events):
    """events: time-sorted (kind, t_s, x, y), kind m=move d=left press x=reset (release/drag/other button).
    Returns point-to-click movements: the continuous burst of moves before each press (>=1 move)."""
    out, moves = [], []
    for k, t, x, y in events:
        if k == "m":
            if moves and t - moves[-1][0] > GAP:
                moves = []
            moves.append((t, x, y))
        elif k == "d":
            if moves:
                out.append({"pts": moves, "t_down": t})
            moves = []
        elif k == "x":
            moves = []
    return out


def features(seg):
    t, x, y = (np.array(c, float) for c in zip(*seg["pts"]))
    t, idx = np.unique(t, return_index=True)  # duplicate timestamps: keep first
    x, y = x[idx], y[idx]
    dur = t[-1] - t[0]
    if len(t) > 1 and dur > 0:
        g = np.arange(t[0], t[-1] + 1e-9, 1 / RATE)
        x, y = np.interp(g, t, x), np.interp(g, t, y)
    else:
        x, y = x[-1:], y[-1:]
    dx, dy = np.diff(x), np.diff(y)
    step = np.hypot(dx, dy)
    L = step.sum()
    disp = math.hypot(x[-1] - x[0], y[-1] - y[0])
    v = step * RATE
    a = np.diff(v) * RATE
    j = np.diff(a) * RATE
    th = np.arctan2(dy[step > 0], dx[step > 0])
    dth = np.abs((np.diff(th) + np.pi) % (2 * np.pi) - np.pi)
    return {"samples": len(x), "duration_s": float(dur), "straightness": float(disp / L) if L > 0 else 1.0,
            "v_mean": float(v.mean()) if len(v) else 0.0, "v_std": float(v.std()) if len(v) else 0.0,
            "a_std": float(a.std()) if len(a) else 0.0, "jerk_mean": float(np.abs(j).mean()) if len(j) else 0.0,
            "curvature": float(dth.sum() / L) if L > 0 else 0.0,
            "pause_s": float(seg["t_down"] - seg["pts"][-1][0]), "travel_px": disp}


def load_balabit(root):
    """{user: [segment, ...]} from training_files/<user>/session_*. Columns: record ts, client ts, button, state, x, y."""
    out = {}
    for sess in sorted(glob.glob(os.path.join(root, "training_files", "user*", "session_*"))):
        ev = []
        with open(sess) as f:
            for r in csv.DictReader(f):
                st, btn = r["state"], r["button"]
                k = "m" if st == "Move" else "d" if (st == "Pressed" and btn == "Left") else "x"
                ev.append((k, float(r["client timestamp"]), int(float(r["x"])), int(float(r["y"]))))
        ev.sort(key=lambda e: e[1])
        out.setdefault(sess.split(os.sep)[-2], []).extend(segments(ev))
    return out


def synthetic_bot(seg, rng):
    """Scripted movement between the human segment's endpoints: teleport or constant-velocity line at 60 Hz."""
    (t0, x0, y0), (_, x1, y1) = seg["pts"][0], seg["pts"][-1]
    pause = rng.uniform(0.0, 0.1)
    if rng.random() < 0.5:
        return {"pts": [(t0, x1, y1)], "t_down": t0 + pause}
    n = max(2, int(rng.uniform(0.1, 0.8) * 60))
    pts = [(t0 + i / 60, round(x0 + (x1 - x0) * i / (n - 1)), round(y0 + (y1 - y0) * i / (n - 1))) for i in range(n)]
    return {"pts": pts, "t_down": pts[-1][0] + pause}


def is_bot(f, rule):
    return f["samples"] < rule["N"] or f["straightness"] > rule["S"]


def fit_rule(X, y):
    """Grid search (N, S) maximising accuracy. X: feature dicts, y: 1 = bot."""
    n = np.array([f["samples"] for f in X])
    s = np.array([f["straightness"] for f in X])
    y = np.array(y, bool)
    best = None
    for N in range(1, 16):
        for S in np.round(np.arange(0.90, 1.0001, 0.0025), 4):
            acc = np.mean(((n < N) | (s > S)) == y)
            if best is None or acc > best[0]:
                best = (acc, {"N": N, "S": float(S)})
    return best[1]


def train(balabit_root, seed=0):
    rng = random.Random(seed)
    users = load_balabit(balabit_root)
    split = {"train": ([], []), "test": ([], [])}
    for u, segs in sorted(users.items()):
        X, y = split["test" if u in TEST_USERS else "train"]
        for s in segs:
            f = features(s)
            if f["travel_px"] < MIN_TRAVEL:
                continue
            X.append(f), y.append(0)
            X.append(features(synthetic_bot(s, rng))), y.append(1)
    rule = fit_rule(*split["train"])
    Xt, yt = split["test"]
    pred = [is_bot(f, rule) for f in Xt]
    hum = [p for p, t in zip(pred, yt) if t == 0]
    bot = [p for p, t in zip(pred, yt) if t == 1]
    return {"rule": rule, "rate_hz": RATE, "gap_s": GAP, "min_travel_px": MIN_TRAVEL,
            "train_users": sorted(set(users) - TEST_USERS), "test_users": sorted(TEST_USERS),
            "n_train": len(split["train"][1]), "n_test": len(yt),
            "test_accuracy": float(np.mean([p == bool(t) for p, t in zip(pred, yt)])),
            "test_human_flagged": float(np.mean(hum)), "test_bot_flagged": float(np.mean(bot)),
            "_test_human": [f for f, t in zip(Xt, yt) if t == 0], "_test_bot": [f for f, t in zip(Xt, yt) if t == 1]}


def browser_segments(kin_lines):
    """{run_id: [segment, ...]} from logs/kinematics.jsonl lines (t in ms, one page per line)."""
    pages = {}
    for e in kin_lines:
        pages.setdefault((e["run"], e["page"]), []).extend(e["ev"])
    out = {}
    for (run, _), ev in pages.items():
        ev = sorted(((k, t / 1000, x, y) for k, t, x, y in ev if k in "md"), key=lambda e: e[1])
        out.setdefault(run, []).extend(segments(ev))
    return out


def summarize(fs, rule):
    med = lambda k: float(np.median([f[k] for f in fs])) if fs else None
    return {"movements": len(fs), "flagged_bot": sum(is_bot(f, rule) for f in fs),
            **{f"median_{k}": med(k) for k in ("samples", "straightness", "duration_s", "pause_s", "v_std")}}


def selfcheck():
    line = {"pts": [(i / 100, 10 + 5 * i, 20) for i in range(41)], "t_down": 0.55}
    arc = {"pts": [(i / 100, 100 + 100 * math.cos(math.pi * i / 40), 100 * math.sin(math.pi * i / 40)) for i in range(41)],
           "t_down": 0.6}
    fl, fa = features(line), features(arc)
    assert abs(fl["straightness"] - 1) < 1e-9 and fl["curvature"] < 1e-9 and fl["samples"] == 21, fl  # 0.4 s at 50 Hz
    assert abs(fl["v_mean"] - 500) < 1e-6 and fl["v_std"] < 1e-6 and abs(fl["pause_s"] - 0.15) < 1e-9, fl
    assert abs(fa["straightness"] - 2 / math.pi) < 0.01 and fa["curvature"] > 0.009, fa  # semicircle: 2/pi, 1/r
    tele = features({"pts": [(0.0, 50, 50)], "t_down": 0.05})
    assert tele["samples"] == 1 and tele["straightness"] == 1.0
    rule = {"N": 3, "S": 0.99}
    assert is_bot(fl, rule) and is_bot(tele, rule) and not is_bot(fa, rule)
    ev = [("m", 0.0, 0, 0), ("m", 0.1, 5, 5), ("m", 2.0, 9, 9), ("m", 2.02, 10, 10), ("d", 2.1, 10, 10),
          ("d", 3.0, 10, 10), ("m", 3.1, 20, 20), ("x", 3.2, 20, 20), ("m", 4.0, 1, 1), ("d", 4.1, 1, 1)]
    s = segments(ev)  # gap > 1 s cuts the first burst; press without moves and moves before a reset are dropped
    assert [len(x["pts"]) for x in s] == [2, 1] and s[0]["pts"][0][1:] == (9, 9), s
    assert fit_rule([fl, tele, fa], [1, 1, 0])["S"] < 1.0
    rng = random.Random(1)
    b = [features(synthetic_bot(arc, rng)) for _ in range(20)]
    assert all(is_bot(f, {"N": 3, "S": 0.99}) for f in b), b
