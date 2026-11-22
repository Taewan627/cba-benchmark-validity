#!/usr/bin/env python3
"""
Figure 4 — Conservative CLEAN false-positive rate across benchmarks
------------------------------------------------------------
Standalone, self-contained script (no external style module needed).
Requires: matplotlib >= 3.5
Run:      python3 fig4_clean_fpr.py
Outputs:  fig4_clean_fpr.pdf (vector, for LaTeX/Word) and fig4_clean_fpr.png (600 dpi)
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


labels = ["Study 2 v1\n50/120", "Study 2b\n1/120"]
vals = [41.7, 0.83]
colors = [RUST, GREEN_OK]

fig, ax = plt.subplots(figsize=(3.4, 3.15))
x = np.arange(2)
bars = ax.bar(x, vals, width=0.5, color=colors, edgecolor="none", zorder=3)

for xi, v in zip(x, vals):
    ax.text(xi, v + 1.3, f"{v:.2f}%".rstrip("0").rstrip(".") + "%" if False else f"{v:g}%",
            ha="center", va="bottom", fontsize=9.5, fontweight="bold", color="#222222")

ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=8.3)
ax.set_ylabel("Conservative CLEAN false-positive rate (%)", fontsize=8.6)
ax.set_ylim(0, 50)
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(axis="both", length=3)
ax.set_axisbelow(True)
ax.yaxis.grid(True, color="#E5E5E5", linewidth=0.7, zorder=0)

ax.set_title("Conservative CLEAN FPR across benchmarks", fontsize=9.3, fontweight="bold", pad=10)
fig.text(0.55, 0.015, "Descriptive comparison across different benchmarks;\nno causal repair effect is estimated.",
          ha="center", fontsize=7.2, style="italic", color=SLATE, linespacing=1.4)

plt.tight_layout(rect=[0, 0.09, 1, 1])
plt.savefig("fig4_clean_fpr.pdf", dpi=600, bbox_inches="tight")
plt.savefig("fig4_clean_fpr.png", dpi=600, bbox_inches="tight")
print("fig4 done")
