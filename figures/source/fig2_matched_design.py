#!/usr/bin/env python3
"""
Figure 2 — Same-obligation matched design (CLEAN/COMMISSION/OMISSION)
------------------------------------------------------------
Standalone, self-contained script (no external style module needed).
Requires: matplotlib >= 3.5
Run:      python3 fig2_matched_design.py
Outputs:  fig2_matched_design.pdf (vector, for LaTeX/Word) and fig2_matched_design.png (600 dpi)
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

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


fig, ax = plt.subplots(figsize=(7.16, 3.35))
ax.set_xlim(0, 100)
ax.set_ylim(0, 46)
ax.axis("off")

# --- Root box ---
root_w, root_h = 46, 7.5
root_x, root_y = 50 - root_w / 2, 33.5
root = FancyBboxPatch((root_x, root_y), root_w, root_h,
                       boxstyle="round,pad=0.25,rounding_size=1.1",
                       linewidth=1.4, edgecolor=INK, facecolor="#F4F5F7", zorder=3)
ax.add_patch(root)
ax.text(50, root_y + root_h / 2, "One base case: fixed audited obligation  $R$",
        ha="center", va="center", fontsize=9.3, fontweight="bold", color=INK, zorder=4)

# --- Three child boxes ---
children = [
    dict(title="CLEAN", ec=NAVY, fc="#EAF0F7",
         lines=["Required event occurs.", "No incompatible event."],
         oracle="Oracle: nonviolation"),
    dict(title="COMMISSION", ec=RUST, fc="#FBEFEA",
         lines=["Incompatible event occurs.", "Required event absent."],
         oracle="Oracle: violation"),
    dict(title="OMISSION", ec="#6D5A9E", fc="#F0EDF6",
         lines=["Required event absent.", "No incompatible event."],
         oracle="Oracle: violation"),
]

n = 3
box_w = 27
gap = (100 - n * box_w) / (n + 1)
xs = [gap + i * (box_w + gap) for i in range(n)]
y0, box_h = 4.5, 17.5
cy_top = y0 + box_h

for x, c in zip(xs, children):
    box = FancyBboxPatch((x, y0), box_w, box_h,
                          boxstyle="round,pad=0.22,rounding_size=1.0",
                          linewidth=1.5, edgecolor=c["ec"], facecolor=c["fc"], zorder=3)
    ax.add_patch(box)
    ax.text(x + box_w / 2, y0 + box_h - 2.4, c["title"], ha="center", va="top",
            fontsize=10, fontweight="bold", color=c["ec"], zorder=4)
    body = "\n".join(c["lines"])
    ax.text(x + box_w / 2, y0 + box_h / 2 - 0.5, body, ha="center", va="center",
            fontsize=7.9, color="#333333", linespacing=1.7, zorder=4)
    ax.text(x + box_w / 2, y0 + 2.1, c["oracle"], ha="center", va="bottom",
            fontsize=7.4, color=c["ec"], style="italic", zorder=4)

    arr = FancyArrowPatch((50, root_y - 0.1), (x + box_w / 2, cy_top + 0.2),
                           arrowstyle="-|>", mutation_scale=9,
                           linewidth=1.1, color="#666666",
                           connectionstyle="arc3,rad=0.0", zorder=1,
                           shrinkA=2, shrinkB=2)
    ax.add_patch(arr)

ax.text(50, 43.5, "Same-obligation matched design", ha="center", va="center",
        fontsize=10.5, fontweight="bold", color=INK)
ax.text(50, 1.3, "Obligation, target position, and non-target beats are matched; perceived salience is not assumed equal.",
        ha="center", va="center", fontsize=7.4, style="italic", color=SLATE)

plt.tight_layout(pad=0.3)
plt.savefig("fig2_matched_design.pdf", dpi=600, bbox_inches="tight")
plt.savefig("fig2_matched_design.png", dpi=600, bbox_inches="tight")
print("fig2 done")
