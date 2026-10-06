#!/usr/bin/env python3
"""
Figure 1 — Study sequence and frozen decisions (flow diagram)
------------------------------------------------------------
Standalone, self-contained script (no external style module needed).
Requires: matplotlib >= 3.5
Run:      python3 fig1_study_sequence.py
Outputs:  fig1_study_sequence.pdf (vector, for LaTeX/Word) and fig1_study_sequence.png (600 dpi)
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import textwrap

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


fig, ax = plt.subplots(figsize=(7.4, 2.3))
ax.set_xlim(0, 100)
ax.set_ylim(9, 38)
ax.axis("off")

boxes = [
    dict(title="Study 1", lines=["P1\u2013P4,", "held-out confirmation"],
         status="INCONCLUSIVE", fc=WHITE, ec=NAVY, tc=NAVY),
    dict(title="Study 2 v1", lines=["POINT vs. SCOPE,", "explicit-rule audit"],
         status="INCONCLUSIVE", fc=WHITE, ec=NAVY, tc=NAVY),
    dict(title="CLEAN quality\nfailure", lines=["Conservative FPR", "50/120 = 41.7%"],
         status="GATE FAILED", fc="#FBEEE9", ec=RUST, tc=RUST),
    dict(title="Post-hoc\nauthor audit", lines=["Benchmark, ambiguity,", "parser, evaluator"],
         status="DIAGNOSTIC", fc=WHITE, ec=SLATE, tc=SLATE),
    dict(title="Study 2b", lines=["60 fresh cases,", "frozen pre-execution"],
         status="360/360 CALLS", fc=WHITE, ec=NAVY, tc=NAVY),
    dict(title="Final result", lines=["\u0394 = +0.017", "95% CI [\u22120.033, 0.067]"],
         status="+0.15 EXCLUDED", fc="#EAF2EC", ec=GREEN_OK, tc="#1E6E5C"),
]

n = len(boxes)
box_w = 13.2
gap = (100 - n * box_w) / (n + 1)
xs = [gap + i * (box_w + gap) for i in range(n)]
y0, box_h = 12.5, 17.5
cy = y0 + box_h / 2

for i, (x, b) in enumerate(zip(xs, boxes)):
    box = FancyBboxPatch(
        (x, y0), box_w, box_h,
        boxstyle="round,pad=0.22,rounding_size=1.0",
        linewidth=1.3, edgecolor=b["ec"], facecolor=b["fc"], zorder=2,
        mutation_aspect=1,
    )
    ax.add_patch(box)

    ax.text(x + box_w / 2, y0 + box_h - 1.6, b["title"],
            ha="center", va="top", fontsize=8.4, fontweight="bold",
            color=b["tc"], linespacing=1.3, zorder=3)

    body = "\n".join(b["lines"])
    ax.text(x + box_w / 2, cy - 1.1, body,
            ha="center", va="center", fontsize=7.5, color="#333333",
            linespacing=1.6, zorder=3)

    status_wrapped = "\n".join(textwrap.wrap(b["status"], width=13))
    ax.text(x + box_w / 2, y0 + 2.3, status_wrapped,
            ha="center", va="bottom", fontsize=6.5, color=b["tc"],
            fontweight="bold", linespacing=1.3, zorder=3)

    if i < n - 1:
        x_next = xs[i + 1]
        arr = FancyArrowPatch(
            (x + box_w + 0.2, cy), (x_next - 0.2, cy),
            arrowstyle="-|>", mutation_scale=10,
            linewidth=1.2, color="#4B4B4B", zorder=1,
        )
        ax.add_patch(arr)

ax.text(50, 34.5, "Study sequence and frozen decisions", ha="center", va="center",
        fontsize=10, fontweight="bold", color=INK)
ax.text(50, 31.2, "No positive mechanism confirmation is implied by this sequence",
        ha="center", va="center", fontsize=8, style="italic", color=SLATE)

plt.tight_layout(pad=0.4)
plt.savefig("fig1_study_sequence.pdf", dpi=600, bbox_inches="tight")
plt.savefig("fig1_study_sequence.png", dpi=600, bbox_inches="tight")
print("fig1 done")
