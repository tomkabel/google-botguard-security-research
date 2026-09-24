"""Shared run logging. One JSONL line per run in logs/runs-<config>.jsonl.

Record: {run_id, config, model, start, end, success, actions:[{t, kind, dur_s}],
         input_tokens, output_tokens, error}
"""
import json, os, time, uuid

# RUN_LOG_DIR keeps experiment runs (logs/xsite, logs/kin) out of the base tables (logs/runs-*.jsonl).
LOGDIR = os.environ.get("RUN_LOG_DIR") or os.path.join(os.path.dirname(__file__), "..", "logs")
BASE = os.environ.get("TESTBED_URL", "http://127.0.0.1:8799")
# Hard scope guard: attackers only ever target the local testbed.
assert BASE.startswith(("http://127.0.0.1", "http://localhost")), "testbed must be local"
# Experiment B: FLOW_PREFIX=/v/<k> points an unmodified agent at variant k (flow at {BASE}{FLOW}/1).
PREFIX = os.environ.get("FLOW_PREFIX", "")
assert PREFIX == "" or PREFIX.startswith("/v/"), "FLOW_PREFIX must be /v/<k>"
FLOW = f"{PREFIX}/flow"
FLOW_ANSWERS = ["Test User", "test@example.invalid", "Tartu", "50090", "YES"]


class Run:
    def __init__(self, config, model=None):
        self.r = {"run_id": f"{config}-{uuid.uuid4().hex[:8]}", "config": config, "model": model,
                  "start": time.time(), "actions": [], "input_tokens": 0, "output_tokens": 0,
                  "success": False, "error": None}
        if PREFIX:
            self.r["variant"] = int(PREFIX.split("/")[2])
        self._t = time.time()

    @property
    def id(self):
        return self.r["run_id"]

    def act(self, kind):
        now = time.time()
        self.r["actions"].append({"t": now, "kind": kind, "dur_s": now - self._t})
        self._t = now

    def tokens(self, inp, out):
        self.r["input_tokens"] += inp
        self.r["output_tokens"] += out

    def save(self):
        self.r["end"] = time.time()
        os.makedirs(LOGDIR, exist_ok=True)
        with open(os.path.join(LOGDIR, f"runs-{self.r['config']}.jsonl"), "a") as f:
            f.write(json.dumps(self.r) + "\n")
        return self.r
