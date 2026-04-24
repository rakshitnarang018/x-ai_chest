"""
Central configuration for Multi-Domain XAI Radiology Assistant
--------------------------------------------------------------

Single source of truth for:

- Model paths
- Class mappings
- Image dimensions
- Confidence thresholds
- LIME parameters
- Background worker settings
- Phi3 / Ollama config
- API limits
"""

from pathlib import Path
import os

# =========================================================
# BASE PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

APP_DIR = BASE_DIR / "app"
MODEL_DIR = BASE_DIR / "saved_models"

UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

TEMP_DIR = BASE_DIR / "temp"
TEMP_DIR.mkdir(exist_ok=True)


# =========================================================
# MODEL PATHS
# =========================================================

TYPE_CLASSIFIER_PATH = MODEL_DIR / "type_classifier.keras"

CHEST_MODEL_PATH = MODEL_DIR / "chest_final.keras"
BONE_MODEL_PATH = MODEL_DIR / "bone_final.keras"
KNEE_MODEL_PATH = MODEL_DIR / "knee_final.keras"
DENTAL_MODEL_PATH = MODEL_DIR / "dental_final.keras"


# =========================================================
# MODEL LABEL MAPS
# =========================================================

TYPE_CLASSES = {
    "bone": 0,
    "chest": 1,
    "dental": 2,
    "knee": 3
}
TYPE_IDX_TO_LABEL = {v: k for k, v in TYPE_CLASSES.items()}


CHEST_CLASSES = {
    "CARDIOMEGALY": 0,
    "COVID19": 1,
    "EFFUSION": 2,
    "NORMAL": 3,
    "PNEUMONIA": 4,
    "PNEUMOTHORAX": 5,
    "TUBERCULOSIS": 6
}
CHEST_IDX_TO_LABEL = {v: k for k, v in CHEST_CLASSES.items()}


BONE_CLASSES = {
    "FRACTURE": 0,
    "NORMAL": 1
}
BONE_IDX_TO_LABEL = {v: k for k, v in BONE_CLASSES.items()}


KNEE_CLASSES = {
    "NORMAL": 0,
    "OSTEOPOROSIS": 1
}
KNEE_IDX_TO_LABEL = {v: k for k, v in KNEE_CLASSES.items()}


# Binary patch classifier
DENTAL_CLASSES = {
    "NORMAL": 0,
    "CAVITY": 1
}
DENTAL_IDX_TO_LABEL = {v: k for k, v in DENTAL_CLASSES.items()}


# =========================================================
# IMAGE CONFIG
# =========================================================

IMG_HEIGHT = 224
IMG_WIDTH = 224

IMG_SIZE = (IMG_HEIGHT, IMG_WIDTH)

CHANNELS = 3

MODEL_INPUT_SHAPE = (
    1,
    IMG_HEIGHT,
    IMG_WIDTH,
    CHANNELS
)

STANDARD_IMAGE_DTYPE = "float32"

ALLOWED_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg"
}

MAX_UPLOAD_MB = 20


# =========================================================
# DENTAL PATCH DETECTION CONFIG
# =========================================================

DENTAL_INPUT_SIZE = (512, 512)

PATCH_SIZE = 224
PATCH_STRIDE = 112

PATCH_STD_THRESHOLD = 15

TOP_PATCH_RATIO = 0.40

DENTAL_DETECTION_THRESHOLD = 0.60


# =========================================================
# PREDICTION THRESHOLDS
# =========================================================

LOW_CONFIDENCE_THRESHOLD = 0.60

HIGH_CONFIDENCE_THRESHOLD = 0.85


# Severity heuristics
SEVERITY_THRESHOLDS = {
    "mild": 0.65,
    "moderate": 0.80,
    "severe": 0.90
}


# =========================================================
# LIME CONFIG
# =========================================================

ENABLE_LIME_DEFAULT = False

LIME_NUM_SAMPLES = 300
LIME_NUM_FEATURES = 5

LIME_RESIZE = 128

LIME_HIDE_COLOR = 0


# =========================================================
# GRADCAM CONFIG
# =========================================================

GRADCAM_ALPHA = 0.4


# =========================================================
# BACKGROUND EXECUTION
# =========================================================

MAX_WORKERS = 4

JOB_POLL_INTERVAL_SECONDS = 2

JOB_TIMEOUT_SECONDS = 120


# =========================================================
# CACHE SETTINGS
# =========================================================

ENABLE_IMAGE_HASH_CACHE = False

CACHE_MAX_ITEMS = 500


# =========================================================
# OLLAMA / PHI3 CONFIG
# =========================================================

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434"
)

LLM_MODEL_NAME = "phi3"

LLM_TIMEOUT_SECONDS = 120


# =========================================================
# FASTAPI APP SETTINGS
# =========================================================

API_TITLE = "Multi-Domain XAI Radiology Assistant"

API_VERSION = "1.0.0"

DEBUG = True


# =========================================================
# LOGGING
# =========================================================

LOG_LEVEL = "INFO"


# =========================================================
# HEALTH CHECK
# =========================================================

HEALTH_CHECK_MODELS_REQUIRED = [
    "type_classifier",
    "chest",
    "bone",
    "knee",
    "dental"
]


# =========================================================
# HELPERS
# =========================================================

def get_severity_from_confidence(confidence: float) -> str:
    """
    Simple confidence-based severity heuristic.
    Can later be disease-specific.
    """

    if confidence >= SEVERITY_THRESHOLDS["severe"]:
        return "severe"

    if confidence >= SEVERITY_THRESHOLDS["moderate"]:
        return "moderate"

    return "mild"


def is_allowed_file(filename: str) -> bool:
    ext = Path(filename).suffix.lower()
    return ext in ALLOWED_EXTENSIONS