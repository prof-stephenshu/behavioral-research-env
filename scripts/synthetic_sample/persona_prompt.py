"""
Builds subject-facing prompts for Stage 4, in two modes:

  - "api" mode (used by run_subjects.py): build_call() returns a per-subject
    system prompt, user message, and a forced-output tool schema for a direct
    Anthropic API call. Requires ANTHROPIC_API_KEY.

  - "subagent" mode (used by build_batches.py, the default): build_batch_prompt()
    returns one self-contained text prompt covering a batch of subjects, meant
    to be handed to a Claude Code subagent (via the Agent tool) with no API key
    required. The subagent is asked to return a JSON array in its final message
    instead of making a forced tool call, since subagents don't expose that
    mechanism to the orchestrating skill.

Kept separate from the calling/orchestration scripts so the prompt construction
(the part most likely to need tuning per project) can be edited without
touching concurrency or Agent-tool orchestration logic.
"""

import json

DEMOGRAPHIC_LABELS = {
    "age": "age",
    "gender": "gender",
    "income": "annual income",
    "education": "education level",
    "population": "population/location",
}


def _format_profile(row, variable_meta):
    """Render a subject's sampled variables as a plain-language profile block."""
    lines = []
    for var in variable_meta:
        name = var["name"]
        if name not in row:
            continue
        value = row[name]
        label = DEMOGRAPHIC_LABELS.get(name, name.replace("_", " "))
        if var["kind"] == "continuous":
            value = round(float(value), 2)
        lines.append(f"- {label}: {value}")
    return "\n".join(lines)


def build_system_prompt(row, variable_meta):
    profile = _format_profile(row, variable_meta)
    return (
        "You are role-playing as a single real human research participant in a "
        "behavioral science study, not an idealized rational agent and not an AI "
        "assistant. You have been assigned the following profile, drawn at random "
        "from a realistic population distribution:\n\n"
        f"{profile}\n\n"
        "Respond the way a real person with this specific profile plausibly would: "
        "let their numeracy, financial literacy, loss aversion, present bias, "
        "personality, and other traits described above shape how much they read, "
        "how they weigh gains/losses, and what they ultimately decide. People with "
        "different profiles should often reach different decisions and give different "
        "reasoning -- do not default to the same 'reasonable' answer regardless of "
        "profile. You must respond only by calling the record_response tool."
    )


def build_user_message(stimulus_text, outcome_variable):
    desc = outcome_variable.get("description", "")
    return (
        "Here is what you are looking at:\n\n"
        f"{stimulus_text}\n\n"
        f"{desc}\n\n"
        "Decide how you, as this person, respond, and briefly explain your reasoning "
        "in your own voice."
    )


def build_tool_schema(outcome_variable):
    """
    outcome_variable schema (from test_config.json):
      binary/categorical: {"name": ..., "type": "binary", "options": [...], "description": ...}
      continuous:         {"name": ..., "type": "continuous", "scale_min": 0, "scale_max": 10, "description": ...}
    Secondary DVs (optional list under "secondary") follow the same shape and are
    added as extra required tool properties.
    """
    properties = {}
    required = []

    def add_dv(dv):
        field = dv["name"]
        if dv["type"] in ("binary", "categorical"):
            properties[field] = {
                "type": "string",
                "enum": dv["options"],
                "description": dv.get("description", ""),
            }
        else:
            prop = {"type": "number", "description": dv.get("description", "")}
            if "scale_min" in dv:
                prop["minimum"] = dv["scale_min"]
            if "scale_max" in dv:
                prop["maximum"] = dv["scale_max"]
            properties[field] = prop
        required.append(field)

    add_dv(outcome_variable)
    for dv in outcome_variable.get("secondary", []):
        add_dv(dv)

    properties["reasoning"] = {
        "type": "string",
        "description": "Brief first-person explanation of why you decided this.",
    }
    required.append("reasoning")

    return {
        "name": "record_response",
        "description": "Record this subject's decision and reasoning.",
        "input_schema": {
            "type": "object",
            "properties": properties,
            "required": required,
        },
    }


def build_call(row, variable_meta, stimulus_text, outcome_variable):
    """Returns (system_prompt, messages, tool_schema) ready to pass to the Anthropic API."""
    system = build_system_prompt(row, variable_meta)
    user_message = build_user_message(stimulus_text, outcome_variable)
    tool_schema = build_tool_schema(outcome_variable)
    messages = [{"role": "user", "content": user_message}]
    return system, messages, tool_schema


# ---------------------------------------------------------------------------
# Subagent (batch) mode -- no API key, no forced tool_choice. The subagent is
# instructed to end its reply with a JSON array; the orchestrating skill parses it.
# ---------------------------------------------------------------------------

def _dv_list(outcome_variable):
    return [outcome_variable] + list(outcome_variable.get("secondary", []))


def _render_dv_spec(dv):
    if dv["type"] in ("binary", "categorical"):
        return f"  - \"{dv['name']}\": one of {dv['options']} -- {dv.get('description', '')}"
    scale = ""
    if "scale_min" in dv and "scale_max" in dv:
        scale = f" (numeric, {dv['scale_min']}-{dv['scale_max']})"
    return f"  - \"{dv['name']}\": a number{scale} -- {dv.get('description', '')}"


def _example_value(dv):
    if dv["type"] in ("binary", "categorical"):
        return dv["options"][0]
    return dv.get("scale_min", 0)


def _render_subject_block(row, variable_meta):
    profile = _format_profile(row, variable_meta)
    return f"--- Subject {row['subject_id']} (condition: {row['condition']}) ---\n{profile}"


def build_batch_prompt(batch_rows, variable_meta, conditions, outcome_variable):
    """
    batch_rows: list of dicts, each a sampled subject (subject_id, condition, + profile vars)
    conditions: dict of condition_name -> stimulus_text (from test_config.json)
    outcome_variable: primary DV spec, optionally with a "secondary" list of more DVs
    Returns a single prompt string for one Agent-tool invocation covering the whole batch.
    """
    dvs = _dv_list(outcome_variable)

    condition_sections = "\n\n".join(
        f"=== CONDITION: {name} ===\n{text}" for name, text in conditions.items()
    )
    subject_sections = "\n\n".join(_render_subject_block(row, variable_meta) for row in batch_rows)
    dv_spec_lines = "\n".join(_render_dv_spec(dv) for dv in dvs)

    example_obj = {"subject_id": batch_rows[0]["subject_id"]}
    for dv in dvs:
        example_obj[dv["name"]] = _example_value(dv)
    example_obj["reasoning"] = "..."
    example_json = json.dumps([example_obj], indent=2)

    return (
        "You are simulating multiple independent synthetic human research participants "
        "for a behavioral science experiment. Respond in character for each subject "
        "separately and independently: do not let one subject's reasoning bleed into "
        "another's, and expect people with different profiles to genuinely reach "
        "different decisions -- do not default to the same 'reasonable' answer for "
        "everyone regardless of profile. None of these subjects are an AI assistant; "
        "they are ordinary people with the traits described below (numeracy, financial "
        "literacy, loss aversion, present bias, personality, etc. as given).\n\n"
        "Here is what each condition group saw:\n\n"
        f"{condition_sections}\n\n"
        "Here are the subjects to simulate, each already assigned to one of the "
        "conditions above:\n\n"
        f"{subject_sections}\n\n"
        "For each subject, decide how that specific person would respond and report:\n"
        f"{dv_spec_lines}\n"
        "  - \"reasoning\": a brief first-person explanation in that subject's voice\n\n"
        "Respond with ONLY a JSON array, one object per subject, in this exact shape "
        "(one example subject shown), with no text before or after the array:\n\n"
        f"{example_json}"
    )
