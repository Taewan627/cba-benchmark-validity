"""Figure 6: Study 3 per-model ORIG -> REPAIR, primary protocols P1-P3."""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import analyze as A
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.family": "serif", "font.serif": ["Liberation Serif", "DejaVu Serif"], "font.size": 8,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.6})
NAVY, RUST, GREY = "#2b4a6f", "#b5543a", "#9a9a9a"
cases, raw = A.load(); rows, _ = A.score_rows(cases, raw)
labels = {"google/gemini-3.8-flash": "Gemini 3.8 Flash", "anthropic/claude-sonnet-5": "Claude Sonnet 5",
          "openai/gpt-6.1-sol": "GPT-6.1 Sol", "deepseek/deepseek-v4.1-flash-1017": "DeepSeek V4.1 Flash",
          "qwen/qwen3.8-27b": "Qwen3.8 27B"}
def m(arm, cond, ver, field, model=None):
    v = [float(r[field]) for r in rows if r["arm"] == arm and r["cond"] == cond and r["version"] == ver
         and r["protocol"] in A.PRIMARY and (model is None or r["model"] == model)]
    return sum(v) / len(v)
fig, axes = plt.subplots(2, 2, figsize=(7.0, 3.6), sharex=True)
for i, arm in enumerate(("TRIGGER", "STATE")):
    for j, (cond, field, title) in enumerate((("OMISSION", "detected", "OMISSION target recall"),
                                              ("CLEAN", "clean_target_fp", "CLEAN target-rule false-positive rate"))):
        ax = axes[i, j]
        ys = list(range(len(A.MODELS)))[::-1]
        for y, mod in zip(ys, A.MODELS):
            o, r_ = m(arm, cond, "ORIG", field, mod), m(arm, cond, "REPAIR", field, mod)
            ax.plot([o, r_], [y, y], color=GREY, lw=1, zorder=1)
            ax.scatter([o], [y], s=22, facecolor="white", edgecolor=NAVY, lw=1, zorder=2, label="Original" if y == ys[0] else None)
            ax.scatter([r_], [y], s=22, color=RUST, zorder=3, label="Repaired" if y == ys[0] else None)
        po, pr = m(arm, cond, "ORIG", field), m(arm, cond, "REPAIR", field)
        ax.plot([po, pr], [-1.2, -1.2], color="black", lw=1.2)
        ax.scatter([po], [-1.2], s=30, facecolor="white", edgecolor="black", zorder=2)
        ax.scatter([pr], [-1.2], s=30, color="black", zorder=3)
        ax.set_yticks(ys + [-1.2]); ax.set_yticklabels([labels[x] for x in A.MODELS] + ["Pooled"] if j == 0 else [])
        ax.set_xlim(-0.04, 1.04); ax.set_ylim(-1.9, len(A.MODELS) - 0.4)
        ax.axhline(-0.6, color=GREY, lw=0.4, ls=":")
        if i == 0: ax.set_title(title, fontsize=8.5)
        if j == 0: ax.text(-0.62, (len(A.MODELS) - 1) / 2, arm.title() + " arm", rotation=90, va="center",
                           ha="center", transform=ax.get_yaxis_transform(), fontsize=8.5, weight="bold")
        ax.tick_params(length=2, width=0.5)
h, l = axes[0, 0].get_legend_handles_labels()
axes[0, 1].legend(h, l, loc="center right", frameon=False, fontsize=7.5, handletextpad=0.3)
for ax in axes[1]: ax.set_xlabel("Rate (P1-P3, averaged over cases and repetitions)")
fig.tight_layout(w_pad=1.2, h_pad=0.8)
out = Path(__file__).resolve().parents[2] / "manuscript"
fig.savefig(out / "fig6_study3_repair.pdf"); fig.savefig(out / "fig6_study3_repair.png", dpi=300)
print("saved")
