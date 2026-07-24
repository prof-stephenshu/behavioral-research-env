"""
Renders illustrative VS Code + Claude Code chat mockups for the workshop deck/workbook.

These are stylized, generic diagrams -- not real captured screenshots -- and are
labeled as such in every rendered image so they can't be mistaken for an actual
product capture.
"""
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

WINDOW_BG = "#f3f3f3"
SIDEBAR_BG = "#252526"
SIDEBAR_FG = "#d4d4d4"
CHAT_BG = "#ffffff"
USER_BUBBLE = "#d6e4f0"
ASSISTANT_BUBBLE = "#eaeaea"
TITLEBAR = "#dddddd"


def wrap(text, width):
    return "\n".join(textwrap.wrap(text, width))


def render_mockup(out_path, filetree_lines, prompt_text, reply_text, window_title="my-project - Visual Studio Code"):
    fig, ax = plt.subplots(figsize=(10, 6.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.2)
    ax.axis("off")

    # outer window
    ax.add_patch(mpatches.FancyBboxPatch((0.05, 0.05), 9.9, 6.1, boxstyle="round,pad=0.02,rounding_size=0.08",
                                          linewidth=1.2, edgecolor="#999999", facecolor=WINDOW_BG))
    # title bar
    ax.add_patch(mpatches.Rectangle((0.05, 5.75), 9.9, 0.4, facecolor=TITLEBAR, edgecolor="none"))
    for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        ax.add_patch(mpatches.Circle((0.35 + i * 0.25, 5.95), 0.07, facecolor=c, edgecolor="none"))
    ax.text(5.0, 5.95, window_title, ha="center", va="center", fontsize=9.5, color="#333333")

    # sidebar (file tree)
    ax.add_patch(mpatches.Rectangle((0.05, 0.05), 2.3, 5.7, facecolor=SIDEBAR_BG, edgecolor="none"))
    ax.text(0.25, 5.55, "EXPLORER", fontsize=8, color="#999999", fontweight="bold")
    y = 5.25
    for line in filetree_lines:
        ax.text(0.25, y, line, fontsize=8.5, color=SIDEBAR_FG, family="monospace")
        y -= 0.32

    # chat panel (right side)
    chat_x, chat_w = 2.55, 7.2
    ax.add_patch(mpatches.Rectangle((chat_x, 0.05), chat_w, 5.7, facecolor=CHAT_BG, edgecolor="#cccccc", linewidth=0.8))
    ax.text(chat_x + 0.2, 5.55, "Claude Code", fontsize=9.5, color="#555555", fontweight="bold")

    # user message bubble (prompt)
    wrapped_prompt = wrap(prompt_text, 58)
    n_lines_p = wrapped_prompt.count("\n") + 1
    bubble_h_p = 0.32 * n_lines_p + 0.3
    ax.add_patch(mpatches.FancyBboxPatch((chat_x + 1.4, 5.2 - bubble_h_p), chat_w - 1.7, bubble_h_p,
                                         boxstyle="round,pad=0.06,rounding_size=0.12",
                                         linewidth=0, facecolor=USER_BUBBLE))
    ax.text(chat_x + 1.55, 5.2 - bubble_h_p / 2, wrapped_prompt, fontsize=9, va="center", ha="left",
            color="#1a1a1a")

    # assistant reply bubble
    reply_top = 5.2 - bubble_h_p - 0.25
    wrapped_reply = wrap(reply_text, 58)
    n_lines_r = wrapped_reply.count("\n") + 1
    bubble_h_r = 0.32 * n_lines_r + 0.3
    ax.add_patch(mpatches.FancyBboxPatch((chat_x + 0.2, reply_top - bubble_h_r), chat_w - 1.7, bubble_h_r,
                                         boxstyle="round,pad=0.06,rounding_size=0.12",
                                         linewidth=0, facecolor=ASSISTANT_BUBBLE))
    ax.text(chat_x + 0.35, reply_top - bubble_h_r / 2, wrapped_reply, fontsize=9, va="center", ha="left",
            color="#1a1a1a")

    fig.text(0.5, 0.01, "Illustrative mockup -- not an actual screenshot", ha="center",
              fontsize=8.5, style="italic", color="#777777")

    fig.tight_layout(rect=[0, 0.02, 1, 1])
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


BASE_TREE = ["behavioral-", "research-env/", "  .claude/", "    skills/", "  scripts/", "  projects/"]

render_mockup(
    "mockup_setup.png",
    BASE_TREE,
    "Set up a Python virtual environment and install pandas, numpy, and scipy for this project.",
    "Done -- created .venv and installed 3 packages (plus their dependencies). Ready to go.",
)

render_mockup(
    "mockup_stage3.png",
    BASE_TREE + ["    my-study/"],
    "I want to test two landing page headlines. Control: 'Save for retirement today.' "
    "Treatment: 'Protect your family's future, starting now.' Population: US adults, mean age 35. "
    "Outcome: whether they click Sign Up.",
    "Created your design package: research_design.md, stimuli/control.md, stimuli/treatment.md, "
    "population_spec.md, variables_spec.md. Ready for Stage 4 whenever you are.",
)

render_mockup(
    "mockup_stage4.png",
    BASE_TREE + ["    my-study/"],
    "Run the synthetic A/B test. N=200, equal split, batch size 10.",
    "Sampled 200 synthetic subjects and ran 20 batches. subjects_data.csv is ready -- 200 rows, "
    "no missing responses.",
)

render_mockup(
    "mockup_stage5.png",
    BASE_TREE + ["    my-study/"],
    "Run the data analysis: balance check, then a regression on the sign-up decision, plus a bar chart.",
    "Balance looks good across all variables. Treatment significantly increased sign-ups (p<.001). "
    "Chart saved to charts/choice_by_condition.png.",
)

render_mockup(
    "mockup_stage7.png",
    BASE_TREE + ["    my-study/"],
    "Generate the writeup for this project as a Word document.",
    "writeup.docx is ready in 07_writeup/ -- Method, Balance, and Results sections included.",
)

print("Wrote 5 mockup images")
