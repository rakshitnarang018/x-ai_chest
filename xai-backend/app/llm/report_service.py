"""
Phi3 Report Generation Service
------------------------------

Generates structured radiology-style reports.

Uses local Ollama:
model = phi3
"""

import json
import requests

from app.core.config import (
    OLLAMA_BASE_URL,
    LLM_MODEL_NAME,
    LLM_TIMEOUT_SECONDS
)


# ======================================================
# SEVERITY HEURISTIC
# ======================================================

def build_severity_statement(
    label,
    confidence
):
    if label == "Normal":
        return "No significant abnormal severity."

    if confidence >= .90:
        return "High confidence abnormal finding."

    if confidence >= .75:
        return "Moderate confidence abnormal finding."

    return "Low confidence abnormal finding."


# ======================================================
# PROMPT BUILDER
# ======================================================

def build_prompt(
    prediction_payload
):
    label = prediction_payload["label"]
    confidence = prediction_payload["confidence"]
    severity = prediction_payload["severity"]

    severity_statement = (
        build_severity_statement(
            label,
            confidence
        )
    )

    prompt = f"""
You are a radiology assistant.

Return ONLY valid raw JSON.
Do NOT use markdown.
Do NOT wrap response in ```json blocks.

Prediction:
Diagnosis: {label}
Confidence: {confidence:.2f}
Severity: {severity}

Return EXACTLY this schema:

{{
  "findings":"...",
  "impression":"...",
  "limitations":"..."
}}

Requirements:
- concise clinical wording
- mention uncertainty if appropriate
- one limitation only
- valid JSON only

Severity hint:
{severity_statement}
"""

    return prompt.strip()


# ======================================================
# OLLAMA CALL
# ======================================================

def call_phi3(
    prompt
):
    payload = {
        "model": LLM_MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json=payload,
        timeout=LLM_TIMEOUT_SECONDS
    )

    response.raise_for_status()

    result = response.json()

    if "response" in result:
        return result["response"]

    raise ValueError(
        "Unexpected Ollama response"
    )


# ======================================================
# CLEAN MARKDOWN FENCES
# ======================================================

def strip_markdown_fences(
    text
):
    text = text.strip()

    if text.startswith("```json"):
        text = text.replace(
            "```json",
            "",
            1
        )

    if text.startswith("```"):
        text = text.replace(
            "```",
            "",
            1
        )

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


# ======================================================
# SAFE JSON PARSE
# ======================================================

def try_parse_json(
    text
):
    try:
        cleaned = strip_markdown_fences(
            text
        )

        return json.loads(
            cleaned
        )

    except Exception:
        return {
            "findings":
                text.strip(),

            "impression":
                "Generated response not fully structured.",

            "limitations":
                "Formatting inconsistency."
        }


# ======================================================
# FALLBACK REPORT
# ======================================================

def fallback_report(
    prediction_payload
):
    label = prediction_payload["label"]

    if label == "Normal":

        findings = (
            "No significant abnormality detected."
        )

        impression = (
            "Likely normal radiographic appearance."
        )

    else:

        findings = (
            f"Findings suggest {label}."
        )

        impression = (
            f"Model prediction favors {label}."
        )

    return {
        "findings":
            findings,

        "impression":
            impression,

        "limitations":
            "Generated using fallback template."
    }


# ======================================================
# MAIN SERVICE
# ======================================================

def generate_report(
    prediction_payload
):
    """
    Background worker task.
    """

    try:

        prompt = build_prompt(
            prediction_payload
        )

        raw = call_phi3(
            prompt
        )

        parsed = try_parse_json(
            raw
        )

        return {
            "model":
                LLM_MODEL_NAME,

            "generated":
                True,

            "report":
                parsed
        }

    except Exception as e:

        print(
            f"LLM report error: {e}"
        )

        return {
            "model":
                LLM_MODEL_NAME,

            "generated":
                False,

            "report":
                fallback_report(
                    prediction_payload
                )
        }