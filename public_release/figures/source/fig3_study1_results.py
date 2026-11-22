#!/usr/bin/env python3
"""
Figure 3 — Study-1 held-out protocol results (Gemini vs. Claude)
------------------------------------------------------------
Standalone, self-contained script (no external style module needed).
Requires: matplotlib >= 3.5
Run:      python3 fig3_study1_results.py
Outputs:  fig3_study1_results.pdf (vector, for LaTeX/Word) and fig3_study1_results.png (600 dpi)
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# Shared style block (inlined — no external dependency needed)
# ============================================================
NAVY      = "#1D3557"
NAVY_L    = "#4A6FA5"
SLATE     = "#6B7280"
RUST      = "#B5563C"
RUST_L    = "#D98C73"
SAND      = "#E9C46A"
LINE_GRAY = "#9CA3AF"
BG_PANEL  = "#F4F5F7"
INK       = "#1A1A1A"
WHITE     = "#FFFFFF"
GREEN_OK  = "#2A9D8F"

def set_style():
    mpl.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Liberation Serif", "Times New Roman", "DejaVu Serif"],
        "font.size": 9,
        "axes.titlesize": 9.5,
        "axes.labelsize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 7.8,
        "axes.edgecolor": "#333333",
        "axes.linewidth": 0.8,
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": "#333333",
        "ytick.color": "#333333",
        "axes.grid": False,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "mathtext.fontset": "stix",
    })


set_style()


protocols = ["P1", "P2", "P3", "P4"]
data = {
    "Gemini": dict(C=[1.00, 1.00, 0.95, 1.00], O=[0.90, 0.75, 0.85, 0.70],
                   G=[0.100, 0.250, 0.100, 0.300], FPR=[0.150, 0.150, 0.150, 0.000]),
    "Claude": dict(C=[1.00, 1.00, 1.00, 1.00], O=[0.95, 0.85, 0.80, 0.85],
                   G=[0.050, 0.150, 0.200, 0.150], FPR=[0.150, 0.100, 0.100, 0.050]),
}

fig, axes = plt.subplots(1, 2, figsize=(7.16, 3.15), sharey=True)
x = np.arange(len(protocols))
w = 0.32

for ax, (evalr, d) in zip(axes, data.items()):
    b1 = ax.bar(x - w/2, d["G"], width=w, color=NAVY, edgecolor="none",
                label="Commission\u2013omission gap ($G$)", zorder=3)
    b2 = ax.bar(x + w/2, d["FPR"], width=w, color=RUST_L, edgecolor="none",
                label="Conservative CLEAN FPR", zorder=3)

    ax.axhline(0.20, color=RUST, linestyle="--", linewidth=1.1, zorder=2)
    ax.axhline(0.10, color=SLATE, linestyle=":", linewidth=1.1, zorder=2)

    for xi, (c, o) in enumerate(zip(d["C"], d["O"])):
        ax.text(xi, 0.335, f"C={c:.2f}\nO={o:.2f}", ha="center", va="bottom",
                fontsize=6.6, color="#333333", linespacing=1.4)

    ax.set_xticks(x)
    ax.set_xticklabels(protocols, fontsize=8.5)
    ax.set_ylim(0, 0.48)
    ax.set_title(evalr, fontsize=9.5, fontweight="bold", color=INK, pad=12)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(axis="both", length=3)
    ax.set_axisbelow(True)

axes[0].set_ylabel("Rate / gap", fontsize=9)

handles = [
    plt.Rectangle((0, 0), 1, 1, color=NAVY, label="Commission\u2013omission gap ($G$)"),
    plt.Rectangle((0, 0), 1, 1, color=RUST_L, label="Conservative CLEAN FPR"),
    plt.Line2D([0], [0], color=RUST, linestyle="--", linewidth=1.1, label="Ordinary GO gap threshold (0.20)"),
    plt.Line2D([0], [0], color=SLATE, linestyle=":", linewidth=1.1, label="CLEAN FPR limit (0.10)"),
]
fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False,
           fontsize=7.6, bbox_to_anchor=(0.5, 0.0))

fig.subplots_adjust(left=0.08, right=0.98, bottom=0.30, top=0.76, wspace=0.06)

fig.text(0.5, 0.965, "Study-1 held-out protocol results (20 base cases per cell)",
         ha="center", fontsize=9.8, fontweight="bold", color=INK)
fig.text(0.5, 0.905, "Frozen overall decision: INCONCLUSIVE", ha="center",
         fontsize=8.2, style="italic", color=SLATE)
plt.savefig("fig3_study1_results.pdf", dpi=600, bbox_inches="tight")
plt.savefig("fig3_study1_results.png", dpi=600, bbox_inches="tight")
print("fig3 done")
