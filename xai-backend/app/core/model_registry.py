"""
Model Registry
--------------

Loads all models once at application startup and exposes
centralized access for all inference services.

Replaces old model_loader.py
"""

from threading import Lock
from typing import Dict, Any

import tensorflow as tf

from app.core.config import (
    TYPE_CLASSIFIER_PATH,
    CHEST_MODEL_PATH,
    BONE_MODEL_PATH,
    KNEE_MODEL_PATH,
    DENTAL_MODEL_PATH,

    TYPE_IDX_TO_LABEL,
    CHEST_IDX_TO_LABEL,
    BONE_IDX_TO_LABEL,
    KNEE_IDX_TO_LABEL,
    DENTAL_IDX_TO_LABEL
)


class ModelRegistry:
    """
    Singleton-style model registry.
    """

    _models: Dict[str, Any] = {}
    _loaded = False
    _lock = Lock()

    # ---------------------------
    # Load all models
    # ---------------------------
    @classmethod
    def load_models(cls):
        """
        Load all models once.
        Thread-safe.
        """
        if cls._loaded:
            return

        with cls._lock:
            if cls._loaded:
                return

            print("🔵 Loading models...")

            cls._models["type_classifier"] = tf.keras.models.load_model(
                TYPE_CLASSIFIER_PATH
            )

            cls._models["chest"] = tf.keras.models.load_model(
                CHEST_MODEL_PATH
            )

            cls._models["bone"] = tf.keras.models.load_model(
                BONE_MODEL_PATH
            )

            cls._models["knee"] = tf.keras.models.load_model(
                KNEE_MODEL_PATH
            )

            cls._models["dental"] = tf.keras.models.load_model(
                DENTAL_MODEL_PATH
            )

            cls._loaded = True

            print("✅ All models loaded successfully")

    # ---------------------------
    # Generic getter
    # ---------------------------
    @classmethod
    def get_model(cls, name: str):
        if not cls._loaded:
            cls.load_models()

        if name not in cls._models:
            raise ValueError(
                f"Model '{name}' not found in registry"
            )

        return cls._models[name]

    # ---------------------------
    # Typed getters
    # ---------------------------
    @classmethod
    def get_type_classifier(cls):
        return cls.get_model("type_classifier")

    @classmethod
    def get_chest_model(cls):
        return cls.get_model("chest")

    @classmethod
    def get_bone_model(cls):
        return cls.get_model("bone")

    @classmethod
    def get_knee_model(cls):
        return cls.get_model("knee")

    @classmethod
    def get_dental_model(cls):
        return cls.get_model("dental")

    # ---------------------------
    # Label maps
    # ---------------------------
    @staticmethod
    def get_type_labels():
        return TYPE_IDX_TO_LABEL

    @staticmethod
    def get_chest_labels():
        return CHEST_IDX_TO_LABEL

    @staticmethod
    def get_bone_labels():
        return BONE_IDX_TO_LABEL

    @staticmethod
    def get_knee_labels():
        return KNEE_IDX_TO_LABEL

    @staticmethod
    def get_dental_labels():
        return DENTAL_IDX_TO_LABEL

    # ---------------------------
    # Status helpers
    # ---------------------------
    @classmethod
    def is_loaded(cls):
        return cls._loaded

    @classmethod
    def list_models(cls):
        return list(cls._models.keys())

    @classmethod
    def model_status(cls):
        return {
            name: "loaded"
            for name in cls._models.keys()
        }


# ----------------------------------------
# FastAPI startup hook
# ----------------------------------------

def startup_load_models():
    """
    Called on FastAPI startup event.
    """
    ModelRegistry.load_models()


# ----------------------------------------
# Utility inference wrappers
# ----------------------------------------

def predict(model, tensor):
    """
    Standardized prediction wrapper.
    """
    preds = model.predict(
        tensor,
        verbose=0
    )

    return preds


def predict_single(model, tensor):
    """
    Returns single prediction vector.
    """
    preds = predict(model, tensor)

    if len(preds.shape) > 1:
        return preds[0]

    return preds