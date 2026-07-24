"""One-off script to render the three-layer architecture diagram for the workshop deck/workbook."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

fig, ax = plt.subplots(figsize=(11, 7.5))
ax.set_xlim(0, 11)
ax.set_ylim(0, 8)
ax.axis("off")

BOX_STYLE = dict(boxstyle="round,pad=0.4", linewidth=1.5)
LAYER_COLORS = {
    "tools": "#4C72B0",
    "project": "#55A868",
    "external": "#C44E52",
}


def box(x, y, w, h, text, color, fontsize=10.5, fontweight="normal"):
    rect = mpatches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=1.5, edgecolor=color, facecolor="white"
    )
    ax.add_patch(rect)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
             fontsize=fontsize, fontweight=fontweight, color="#222222", wrap=True)
    return (x, y, w, h)


def arrow(b1, b2, side1="bottom", side2="top", color="#888888"):
    x1, y1, w1, h1 = b1
    x2, y2, w2, h2 = b2
    pts = {
        "bottom": (x1 + w1 / 2, y1),
        "top": (x1 + w1 / 2, y1 + h1),
        "left": (x1, y1 + h1 / 2),
        "right": (x1 + w1, y1 + h1 / 2),
    }
    pts2 = {
        "bottom": (x2 + w2 / 2, y2),
        "top": (x2 + w2 / 2, y2 + h2),
        "left": (x2, y2 + h2 / 2),
        "right": (x2 + w2, y2 + h2 / 2),
    }
    p1, p2 = pts[side1], pts2[side2]
    arr = FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=14,
                           color=color, linewidth=1.3, connectionstyle="arc3,rad=0.0")
    ax.add_patch(arr)


# Layer labels
ax.text(0.15, 7.55, "TOOLS", fontsize=11, fontweight="bold", color=LAYER_COLORS["tools"])
ax.text(0.15, 5.05, "PROJECT (behavioral-research-env)", fontsize=11, fontweight="bold", color=LAYER_COLORS["project"])
ax.text(0.15, 2.55, "EXTERNAL SERVICES", fontsize=11, fontweight="bold", color=LAYER_COLORS["external"])

# Tools layer
vscode = box(0.5, 6.3, 3.0, 1.0, "VS Code\n(editor / IDE)", LAYER_COLORS["tools"])
claude = box(4.2, 6.3, 3.0, 1.0, "Claude Code\n(AI agent: reads/writes\nfiles, runs commands)", LAYER_COLORS["tools"])
arrow(vscode, claude, "right", "left", LAYER_COLORS["tools"])
arrow(claude, vscode, "left", "right", LAYER_COLORS["tools"])

# Project layer
skills = box(0.5, 3.8, 2.4, 1.0, "Skills\n.claude/skills/*.md\n(one per stage)", LAYER_COLORS["project"])
scripts = box(3.2, 3.8, 2.4, 1.0, "Python scripts\n(sampling, stats,\ncharts)", LAYER_COLORS["project"])
data = box(5.9, 3.8, 2.4, 1.0, "Project data\nprojects/<slug>/\n(design, test, analysis)", LAYER_COLORS["project"])

arrow(claude, skills, "bottom", "top", "#999999")
arrow(claude, scripts, "bottom", "top", "#999999")
arrow(claude, data, "bottom", "top", "#999999")

# External layer
subagents = box(0.5, 1.3, 2.4, 1.0, "Claude subagents\n(simulated subjects)", LAYER_COLORS["external"])
github = box(3.2, 1.3, 2.4, 1.0, "GitHub\n(version control)", LAYER_COLORS["external"])
pandoc = box(5.9, 1.3, 2.4, 1.0, "pandoc\n(docx / pptx / pdf)", LAYER_COLORS["external"])

arrow(claude, subagents, "left", "top", "#999999")
arrow(data, github, "bottom", "top", "#999999")
arrow(data, pandoc, "bottom", "top", "#999999")

fig.suptitle("Conceptual Architecture", fontsize=15, fontweight="bold", y=0.98)
fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig(r"C:\Users\sds77\behavioral-research-env\presentations\2026-workshop\assets\architecture_diagram.png", dpi=150)
print("Wrote architecture_diagram.png")
