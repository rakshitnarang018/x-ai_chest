"""
Phi3 Report Generation Service
------------------------------

Generates structured radiology-style reports.

Uses local Ollama:
model = phi3

UPDATED
- deterministic normal reports
- modality-aware prompting
- hardened output contract
- guarantees findings/impression/limitations
"""

import json
import requests

from app.core.config import (
    OLLAMA_BASE_URL,
    LLM_MODEL_NAME,
    LLM_TIMEOUT_SECONDS
)



# ======================================================
# NORMAL MODALITY TEMPLATES
# ======================================================

NORMAL_REPORTS = {

    "chest": {
        "findings":
            "Cardiomediastinal silhouette is within normal limits. No focal air-space opacity, pleural effusion, or pneumothorax identified.",

        "impression":
            "No acute cardiopulmonary abnormality detected.",

        "limitations":
            "AI-generated screening support; not a radiologist interpretation."
    },

    "knee": {
        "findings":
            "Alignment is preserved with no radiographic evidence of osteoporosis-related abnormality detected.",

        "impression":
            "No significant osseous abnormality identified on this knee radiograph.",

        "limitations":
            "AI-generated screening support; subtle findings may not be captured."
    },

    "bone": {
        "findings":
            "No radiographic evidence of acute osseous disruption or fracture detected.",

        "impression":
            "No fracture identified on the provided radiograph.",

        "limitations":
            "AI-generated screening support; nondisplaced or subtle fractures may require clinical correlation."
    },

    "dental": {
        "findings":
            "No obvious carious lesion or significant abnormal dental finding detected.",

        "impression":
            "Dental radiograph appears grossly unremarkable.",

        "limitations":
            "AI-generated screening support; clinical correlation recommended."
    }
}



# ======================================================
# SEVERITY HEURISTIC
# ======================================================

def build_severity_statement(
    label,
    confidence
):
    if label=="Normal":
        return "No significant abnormal severity."

    if confidence>=0.90:
        return "High confidence abnormal finding."

    if confidence>=0.75:
        return "Moderate confidence abnormal finding."

    return "Low confidence abnormal finding."



# ======================================================
# PROMPT
# ======================================================

def build_prompt(
    prediction_payload
):
    label=prediction_payload["label"]
    confidence=prediction_payload["confidence"]
    severity=prediction_payload["severity"]
    domain=prediction_payload["domain"]

    severity_statement=(
        build_severity_statement(
            label,
            confidence
        )
    )

    prompt=f"""
You are a specialist radiology assistant.

Return ONLY valid raw JSON.
No markdown.
No code fences.

Imaging modality: {domain}
Predicted diagnosis: {label}
Confidence: {confidence:.2f}
Severity: {severity}

Return EXACTLY:

{{
 "findings":"...",
 "impression":"...",
 "limitations":"..."
}}

Rules:
- modality-specific wording
- concise clinical language
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
    payload={
        "model":LLM_MODEL_NAME,
        "prompt":prompt,
        "stream":False
    }

    response=requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json=payload,
        timeout=LLM_TIMEOUT_SECONDS
    )

    response.raise_for_status()

    result=response.json()

    if "response" in result:
        return result["response"]

    raise ValueError(
        "Unexpected Ollama response"
    )



# ======================================================
# CLEAN MARKDOWN
# ======================================================

def strip_markdown_fences(
    text
):
    text=text.strip()

    if text.startswith(
      "```json"
    ):
        text=text.replace(
            "```json",
            "",
            1
        )

    if text.startswith(
      "```"
    ):
        text=text.replace(
            "```",
            "",
            1
        )

    if text.endswith(
      "```"
    ):
        text=text[:-3]

    return text.strip()



# ======================================================
# SAFE PARSE
# ======================================================

def try_parse_json(
    text
):
    try:

        cleaned=(
            strip_markdown_fences(
                text
            )
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
# CONTRACT HARDENER
# CRITICAL FIX
# ======================================================

def enforce_report_contract(
    parsed,
    prediction_payload
):
    """
    Guarantees all required fields exist.
    Prevents ResponseValidationError.
    """

    fallback=(
        fallback_report(
            prediction_payload
        )
    )

    if not isinstance(
        parsed,
        dict
    ):
        parsed={}

    findings=(
        parsed.get(
            "findings"
        )
        or fallback["findings"]
    )

    impression=(
        parsed.get(
            "impression"
        )
        or fallback["impression"]
    )

    limitations=(
        parsed.get(
            "limitations"
        )
        or fallback["limitations"]
    )

    return {
        "findings":
            findings,

        "impression":
            impression,

        "limitations":
            limitations
    }



# ======================================================
# FALLBACK REPORT
# ======================================================

def fallback_report(
    prediction_payload
):

    label=prediction_payload["label"]
    domain=prediction_payload["domain"]


    if label=="Normal":

        return NORMAL_REPORTS.get(
            domain,
            NORMAL_REPORTS["chest"]
        )


    if domain=="bone":

        return {
            "findings":
                "Radiographic findings are suspicious for fracture or cortical disruption.",

            "impression":
                "Model prediction favors presence of fracture.",

            "limitations":
                "AI-generated screening support; fracture characterization requires expert review."
        }


    return {

        "findings":
            f"Imaging findings suggest {label.lower()}.",

        "impression":
            f"Model prediction favors {label}.",

        "limitations":
            "AI-generated screening support; clinical correlation recommended."
    }



# ======================================================
# MAIN REPORT SERVICE
# ======================================================

def generate_report(
    prediction_payload
):
    """
    Background worker task
    """

    try:

        # ------------------------------
        # deterministic normal reports
        # ------------------------------

        if (
           prediction_payload["label"]
           =="Normal"
        ):

            return {
                "model":
                    "template",

                "generated":
                    True,

                "report":
                    NORMAL_REPORTS[
                     prediction_payload[
                       "domain"
                     ]
                    ]
            }



        # ------------------------------
        # abnormal -> LLM
        # ------------------------------

        prompt=(
            build_prompt(
                prediction_payload
            )
        )


        raw=(
            call_phi3(
                prompt
            )
        )


        parsed=(
            try_parse_json(
                raw
            )
        )


        # ******** FIX ********
        safe_report=(
            enforce_report_contract(
                parsed,
                prediction_payload
            )
        )


        return {

            "model":
                LLM_MODEL_NAME,

            "generated":
                True,

            "report":
                safe_report
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