"""Experiment A: a kinematic (Type III / L1b) detector for point-to-click mouse movements.

Human class: Balabit Mouse Dynamics Challenge training sessions (github.com/balabit/Mouse-Dynamics-Challenge,
clone into measurement/data/). Bot class: synthetic straight-line / teleport movements generated from the
same human endpoints. Agents are scored from logs/kinematics.jsonl (browser mousemove/mousedown events).

Domain shift handling: Balabit is remote-desktop data (client timestamps, ~60 Hz); browser events arrive at
the input rate. Both are resampled by linear interpolation onto one 50 Hz grid before any feature is computed,
so sample count measures duration on a common clock rather than device event rate. Pixels are not rescaled.

Two classifiers, both fitted on training users and reported on held-out users:
  rule: bot iff samples < N or straightness > S, grid-searched against straight/teleport synthetic bots.
  logreg: logistic regression on the full feature vector (numpy Newton/IRLS; scikit-learn is not installable here,
          PEP 668), against a harder bot class: minimum-jerk paths with bow and jitter that copy the paired human's
          duration and pre-click pause. Threshold = 90% TPR on held-out min-jerk bots.
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


def minjerk_bot(seg, rng):
    """Harder bot for the learned classifier: minimum-jerk path between the human segment's endpoints with a random
    lateral bow and Gaussian jitter (sigma 0.5-2 px), 60 Hz, with the paired human's duration and pre-click pause.
    Same generator family as attackers/e_smooth.py, so scoring e-smooth traces with it is an in-distribution test."""
    (t0, x0, y0), (t1, x1, y1) = seg["pts"][0], seg["pts"][-1]
    T, d = max(t1 - t0, 2 / 60), math.hypot(x1 - x0, y1 - y0)
    ux, uy = ((x1 - x0) / d, (y1 - y0) / d) if d else (0, 0)
    bow, sd, n = rng.gauss(0, 0.06) * d, rng.uniform(0.5, 2.0), max(2, int(T * 60))
    pts = []
    for i in range(n + 1):
        tau = i / n
        s = 10 * tau ** 3 - 15 * tau ** 4 + 6 * tau ** 5
        lat = bow * math.sin(math.pi * s)
        jx, jy = (rng.gauss(0, sd), rng.gauss(0, sd)) if 0 < i < n else (0, 0)
        pts.append((t0 + tau * T, round(x0 + s * (x1 - x0) - uy * lat + jx), round(y0 + s * (y1 - y0) + ux * lat + jy)))
    return {"pts": pts, "t_down": pts[-1][0] + seg["t_down"] - seg["pts"][-1][0]}


LOG_FEATURES = [k for k in FEATURES if k != "straightness"]


def vec(f):
    """Feature vector for the logistic regression: log1p of the heavy-tailed features, log(1 - straightness)."""
    return [math.log1p(max(f[k], 0.0)) for k in LOG_FEATURES] + [math.log(1 - min(f["straightness"], 1.0) + 1e-4)]


def fit_logreg(X, y, lam=1.0, iters=30):
    """L2-regularised logistic regression by Newton/IRLS on standardised X. Returns {mu, sd, w} (w[-1] = bias)."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    mu, sd = X.mean(0), X.std(0) + 1e-9
    Z = np.c_[(X - mu) / sd, np.ones(len(X))]
    w = np.zeros(Z.shape[1])
    for _ in range(iters):
        p = 0.5 * (1 + np.tanh(Z @ w / 2))  # overflow-free sigmoid
        H = (Z * (p * (1 - p))[:, None]).T @ Z + lam * np.eye(len(w))
        w -= np.linalg.solve(H, Z.T @ (p - y) + lam * w)
    return {"mu": mu.tolist(), "sd": sd.tolist(), "w": w.tolist()}


def score(fs, clf):
    """Log-odds of 'bot' for feature dicts."""
    X = (np.array([vec(f) for f in fs], float).reshape(len(fs), -1) - clf["mu"]) / clf["sd"]
    return X @ np.array(clf["w"][:-1]) + clf["w"][-1]


def auc(pos, neg):
    """ROC AUC = P(score_bot > score_human), ties count 1/2."""
    neg = np.sort(neg)
    return float(np.mean(np.searchsorted(neg, pos, "left") + np.searchsorted(neg, pos, "right")) / 2 / len(neg))


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
    rng, rng_mj = random.Random(seed), random.Random(seed + 1)  # separate stream keeps the rule's bots unchanged
    users = load_balabit(balabit_root)
    split = {"train": ([], []), "test": ([], [])}
    mj = {"train": [], "test": []}
    for u, segs in sorted(users.items()):
        part = "test" if u in TEST_USERS else "train"
        X, y = split[part]
        for s in segs:
            f = features(s)
            if f["travel_px"] < MIN_TRAVEL:
                continue
            X.append(f), y.append(0)
            X.append(features(synthetic_bot(s, rng))), y.append(1)
            mj[part].append(features(minjerk_bot(s, rng_mj)))
    rule = fit_rule(*split["train"])
    Xh = [f for f, t in zip(*split["train"]) if t == 0]
    clf = fit_logreg([vec(f) for f in Xh + mj["train"]], [0] * len(Xh) + [1] * len(mj["train"]))
    hum_t = [f for f, t in zip(*split["test"]) if t == 0]
    sh, sb = score(hum_t, clf), score(mj["test"], clf)
    clf["threshold"] = float(np.quantile(sb, 0.10))  # flag iff log-odds >= threshold: 90% TPR on held-out bots
    clf.update(features=LOG_FEATURES + ["straightness"], auc=auc(sb, sh), test_bot_tpr=float(np.mean(sb >= clf["threshold"])),
               test_human_fpr=float(np.mean(sh >= clf["threshold"])), n_train=len(Xh) + len(mj["train"]),
               n_test=len(hum_t) + len(mj["test"]))
    Xt, yt = split["test"]
    pred = [is_bot(f, rule) for f in Xt]
    hum = [p for p, t in zip(pred, yt) if t == 0]
    bot = [p for p, t in zip(pred, yt) if t == 1]
    return {"rule": rule, "rate_hz": RATE, "gap_s": GAP, "min_travel_px": MIN_TRAVEL,
            "train_users": sorted(set(users) - TEST_USERS), "test_users": sorted(TEST_USERS),
            "n_train": len(split["train"][1]), "n_test": len(yt),
            "test_accuracy": float(np.mean([p == bool(t) for p, t in zip(pred, yt)])),
            "test_human_flagged": float(np.mean(hum)), "test_bot_flagged": float(np.mean(bot)),
            "classifier": clf, "_test_mj": mj["test"],
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


def summarize(fs, rule, clf=None):
    med = lambda k: float(np.median([f[k] for f in fs])) if fs else None
    extra = {"flagged_clf": int(np.sum(score(fs, clf) >= clf["threshold"])) if fs else 0} if clf else {}
    return {"movements": len(fs), "flagged_bot": sum(is_bot(f, rule) for f in fs), **extra,
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
    assert abs(auc(np.array([2.0, 3.0]), np.array([1.0, 2.0])) - 0.875) < 1e-12  # (1 + 0.5 + 1 + 1) / 4
    # logreg separates wavy human-like arcs from min-jerk paths on the same endpoints
    rng = random.Random(2)
    hum = [{"pts": [(i / 60, 400 * i / 40 + 30 * math.sin(i / 3 + k) + rng.gauss(0, 3), 50 * math.sin(math.pi * i / 40 + k))
                    for i in range(41)], "t_down": 41 / 60 + 0.2} for k in range(40)]
    X = [features(h) for h in hum] + [features(minjerk_bot(h, rng)) for h in hum]
    clf = fit_logreg([vec(f) for f in X], [0] * 40 + [1] * 40)
    s = score(X, clf)
    assert auc(s[40:], s[:40]) > 0.95, auc(s[40:], s[:40])
    mb = minjerk_bot(hum[0], rng)
    assert mb["pts"][0][1:] == (round(hum[0]["pts"][0][1]), round(hum[0]["pts"][0][2])) and abs(mb["t_down"] - hum[0]["t_down"]) < 1e-9
