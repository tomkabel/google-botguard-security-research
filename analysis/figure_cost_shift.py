"""Systematization figure: where the attacker's marginal cost lands, per defense type x attacker class.

Cell values are the authors' assessment, summarising Sections 3.2 and 4.2 of paper.md.
Writes figures/cost_shift.{svg,pdf,png}.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

TYPES = ["I  VM attestation", "II  Stateful telemetry", "III  Behavioral biometrics",
         "IV  Anonymous attestation (HW)", "V  Hardware binding (DBSC/passkeys)"]
ATTACKERS = ["Env. Forgery", "Scripted OS input", "OpSyn VLM", "Hybrid", "Device farm"]
COSTS = ["Forgery / RE", "IP / proxy", "Motor kinematics", "Aged state", "Device / account"]
COLORS = ["#4C78A8", "#F58518", "#54A24B", "#B279A2", "#E45756"]
F, P, K, A, D = range(5)
GRID = [
    [F, P, P, P, D],  # I: forgery cost collapses to IP reputation once the browser is genuine
    [A, A, A, A, D],  # II: aging still required; bought, or met by long-used real devices
    [F, K, K, K, K],  # III: ML/human-farm forgery -> orchestration kinematics
    [D, D, D, D, D],  # IV: modality-independent; cost is enrolled devices/accounts
    [D, D, D, D, D],  # V: same as IV
]


def main():
    assert len(GRID) == len(TYPES) and all(len(r) == len(ATTACKERS) for r in GRID)
    assert all(v in range(len(COSTS)) for r in GRID for v in r)
    fig, ax = plt.subplots(figsize=(7.5, 3.6))
    ax.imshow(GRID, cmap=ListedColormap(COLORS), vmin=0, vmax=len(COSTS) - 1, aspect="auto")
    for i, row in enumerate(GRID):
        for j, v in enumerate(row):
            ax.text(j, i, COSTS[v], ha="center", va="center", fontsize=7, color="white")
    ax.set_xticks(range(len(ATTACKERS)), ATTACKERS, fontsize=8)
    ax.set_yticks(range(len(TYPES)), TYPES, fontsize=8)
    ax.set_xlabel("Attacker class", fontsize=9)
    ax.set_xticks([x - 0.5 for x in range(1, len(ATTACKERS))], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, len(TYPES))], minor=True)
    ax.grid(which="minor", color="white", linewidth=2)
    ax.tick_params(which="both", length=0)
    ax.legend(handles=[Patch(color=c, label=l) for c, l in zip(COLORS, COSTS)],
              loc="upper center", bbox_to_anchor=(0.45, -0.22), ncol=5, fontsize=7, frameon=False)
    fig.tight_layout()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures", "cost_shift")
    for ext in ("svg", "pdf", "png"):
        fig.savefig(f"{out}.{ext}", dpi=200, bbox_inches="tight")


if __name__ == "__main__":
    main()
