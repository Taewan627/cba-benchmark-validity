#!/usr/bin/env python3
"""
Figure 5 — Study-2b pooled results (recall + interaction estimate)
------------------------------------------------------------
Standalone, self-contained script (no external style module needed).
Requires: matplotlib >= 3.5
Run:      python3 fig5_study2b_results.py
Outputs:  fig5_study2b_results.pdf (vector, for LaTeX/Word) and fig5_study2b_results.png (600 dpi)
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


def fmt(v, sign=False, nd=3):
    """Format a number with a typographic minus sign instead of a hyphen."""
    s = f"{v:+.{nd}f}" if sign else f"{v:.{nd}f}"
    return s.replace("-", "\u2212")

fig, axes = plt.subplots(1, 2, figsize=(7.16, 2.85),
                          gridspec_kw={"width_ratios": [1.05, 1.35]})

# ---------- Left panel: recall bars ----------
ax = axes[0]
structs = ["POINT", "SCOPE"]
comm = [0.967, 0.983]
omis = [1.000, 1.000]
x = np.arange(2)
w = 0.32

ax.bar(x - w/2, comm, width=w, color=NAVY, edgecolor="none", label="Commission recall", zorder=3)
ax.bar(x + w/2, omis, width=w, color=RUST_L, edgecolor="none", label="Omission recall", zorder=3)

for xi, g in zip(x, [-0.033, -0.017]):
    ax.text(xi, 1.008, f"$G$ = {fmt(g, sign=True)}", ha="center", va="bottom",
            fontsize=7.6, color="#333333")

ax.set_xticks(x)
ax.set_xticklabels(structs, fontsize=9)
ax.set_ylim(0.86, 1.035)
ax.set_ylabel("Recall", fontsize=9)
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(length=3)
ax.legend(loc="upper center", frameon=False, fontsize=7.5, bbox_to_anchor=(0.5, -0.16), ncol=2)
ax.set_title("Recall by structure", fontsize=9.3, fontweight="bold", pad=10)

# ---------- Right panel: interaction forest plot ----------
ax2 = axes[1]
est, lo, hi = 0.017, -0.033, 0.067
thresh = 0.15

ax2.axvline(0, color="#B0B0B0", linewidth=0.9, zorder=1)
ax2.axvline(thresh, color=RUST, linestyle="--", linewidth=1.2, zorder=1)
ax2.text(thresh, 1.55, "+0.15 practical\nthreshold", color=RUST, fontsize=7.3,
          ha="center", va="bottom", linespacing=1.3, zorder=4,
          bbox=dict(facecolor="white", edgecolor="none", pad=1.6))

ax2.errorbar([est], [1.0], xerr=[[est - lo], [hi - est]], fmt="o",
             color=NAVY, ecolor=NAVY, elinewidth=1.6, capsize=4,
             markersize=6.5, zorder=3)

ax2.set_xlim(-0.09, 0.19)
ax2.set_ylim(0.15, 2.0)
ax2.set_yticks([])
ax2.set_xticks([-0.05, 0, 0.05, 0.10])
ax2.set_xticklabels([fmt(v) for v in [-0.05, 0, 0.05, 0.10]])
ax2.set_xlabel("POINT\u2013SCOPE interaction ($\\Delta_{scope}$, percentage points)", fontsize=8.4)
ax2.spines[["top", "right", "left"]].set_visible(False)
ax2.tick_params(length=3)
ax2.set_title("Pooled interaction estimate", fontsize=9.3, fontweight="bold", pad=10)

ax2.text(est, 0.72, f"$\\Delta$ = {fmt(est, sign=True)}\n95% CI [{fmt(lo)}, {fmt(hi)}]",
          ha="center", va="top", fontsize=7.8, color="#222222", linespacing=1.4,
          zorder=4, bbox=dict(facecolor="white", edgecolor="none", pad=2.2))

fig.text(0.5, 0.965, "Study-2b pooled results (models averaged within case)",
          ha="center", fontsize=10, fontweight="bold", color=INK)
fig.text(0.5, 0.045, "Interval includes zero; smaller interactions remain compatible with the data.",
          ha="center", fontsize=7.6, style="italic", color=SLATE)

plt.tight_layout(rect=[0.01, 0.16, 0.99, 0.89])
plt.savefig("fig5_study2b_results.pdf", dpi=600, bbox_inches="tight")
plt.savefig("fig5_study2b_results.png", dpi=600, bbox_inches="tight")
print("fig5 done")
