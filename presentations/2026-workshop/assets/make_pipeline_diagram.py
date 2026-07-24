"""Renders the 9-stage workflow as a visual pipeline (snake layout), built vs deferred stages color-coded."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

BUILT_COLOR = "#55A868"
DEFERRED_COLOR = "#999999"

STAGES = [
    (1, "Behavioral\naudit", False),
    (2, "Solution\nideation", False),
    (3, "Solution\ndesign", True),
    (4, "Synthetic\nA/B test", True),
    (5, "Data\nanalysis", True),
    (6, "Presentation", False),
    (7, "Scientific\nwriteup", True),
    (8, "Revised\nsolution", False),
    (9, "Feedback", False),
]

fig, ax = plt.subplots(figsize=(12, 5.5))
ax.set_xlim(0, 12)
ax.set_ylim(0, 5.5)
ax.axis("off")

BOX_W, BOX_H = 2.0, 1.3
row1_y, row2_y = 3.6, 1.0
row1_x = [0.4, 2.7, 5.0, 7.3, 9.6]
row2_x = [0.4, 2.7, 5.0, 7.3]

positions = {}
for i in range(5):
    positions[STAGES[i][0]] = (row1_x[i], row1_y)
# row 2 holds stages 6-9, laid out right-to-left so stage 6 sits under stage 5
row2_stage_order = [9, 8, 7, 6]
for i, stage_num in enumerate(row2_stage_order):
    positions[stage_num] = (row2_x[i], row2_y)

boxes = {}
for num, label, built in STAGES:
    x, y = positions[num]
    color = BUILT_COLOR if built else DEFERRED_COLOR
    face = "#eaf5ee" if built else "#f2f2f2"
    rect = mpatches.FancyBboxPatch((x, y), BOX_W, BOX_H, boxstyle="round,pad=0.02,rounding_size=0.1",
                                    linewidth=2 if built else 1.2, edgecolor=color, facecolor=face)
    ax.add_patch(rect)
    ax.text(x + BOX_W / 2, y + BOX_H - 0.28, f"{num}", ha="center", va="center",
            fontsize=13, fontweight="bold", color=color)
    ax.text(x + BOX_W / 2, y + BOX_H / 2 - 0.15, label, ha="center", va="center",
            fontsize=9.5, color="#222222")
    boxes[num] = (x, y, BOX_W, BOX_H)


def arrow(n1, n2, side1, side2):
    x1, y1, w1, h1 = boxes[n1]
    x2, y2, w2, h2 = boxes[n2]
    pts = {
        "right": (x1 + w1, y1 + h1 / 2), "left": (x1, y1 + h1 / 2),
        "bottom": (x1 + w1 / 2, y1), "top": (x1 + w1 / 2, y1 + h1),
    }
    pts2 = {
        "right": (x2 + w2, y2 + h2 / 2), "left": (x2, y2 + h2 / 2),
        "bottom": (x2 + w2 / 2, y2), "top": (x2 + w2 / 2, y2 + h2),
    }
    arr = FancyArrowPatch(pts[side1], pts2[side2], arrowstyle="-|>", mutation_scale=16,
                           color="#666666", linewidth=1.5)
    ax.add_patch(arr)


for a, b in [(1, 2), (2, 3), (3, 4), (4, 5)]:
    arrow(a, b, "right", "left")
arrow(5, 6, "bottom", "top")
for a, b in [(6, 7), (7, 8), (8, 9)]:
    arrow(a, b, "right", "left")

# legend
ax.add_patch(mpatches.FancyBboxPatch((0.4, 4.9), 0.4, 0.3, boxstyle="round,pad=0.02", linewidth=2,
                                      edgecolor=BUILT_COLOR, facecolor="#eaf5ee"))
ax.text(0.95, 5.05, "Built in this workshop", fontsize=10, va="center")
ax.add_patch(mpatches.FancyBboxPatch((3.7, 4.9), 0.4, 0.3, boxstyle="round,pad=0.02", linewidth=1.2,
                                      edgecolor=DEFERRED_COLOR, facecolor="#f2f2f2"))
ax.text(4.25, 5.05, "Deferred", fontsize=10, va="center")

fig.tight_layout()
fig.savefig(r"C:\Users\sds77\behavioral-research-env\presentations\2026-workshop\assets\pipeline_diagram.png", dpi=150)
print("Wrote pipeline_diagram.png")
