"""
Preprocessing Gateway
---------------------

Responsibilities:
- Validate uploads
- Standardize all image inputs
- Convert to canonical internal format
- Generate model-ready tensors
- Reuse image data for prediction + XAI
"""

from pathlib import Path
import hashlib
from typing import Dict, Any

import numpy as np
from PIL import Image, UnidentifiedImageError

from tensorflow.keras.applications.efficientnet import (
    preprocess_input as efficientnet_preprocess
)

from tensorflow.keras.applications.mobilenet_v2 import (
    preprocess_input as mobilenet_preprocess
)

from app.core.config import (
    IMG_SIZE,
    STANDARD_IMAGE_DTYPE,
    ALLOWED_EXTENSIONS,
    MAX_UPLOAD_MB
)


# =====================================================
# VALIDATION
# =====================================================

def validate_file_extension(filename: str):
    ext = Path(filename).suffix.lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {ext}"
        )


def validate_file_size(file_obj):
    """
    Validate upload size.
    Works with FastAPI UploadFile.
    """
    current = file_obj.file.tell()

    file_obj.file.seek(0, 2)
    size_bytes = file_obj.file.tell()

    file_obj.file.seek(current)

    max_bytes = MAX_UPLOAD_MB * 1024 * 1024

    if size_bytes > max_bytes:
        raise ValueError(
            f"File exceeds {MAX_UPLOAD_MB}MB"
        )


# =====================================================
# IMAGE HASHING
# =====================================================

def compute_image_hash(raw_bytes: bytes) -> str:
    return hashlib.sha256(
        raw_bytes
    ).hexdigest()


# =====================================================
# PIL LOAD
# =====================================================

def load_pil_image(file_or_path):
    """
    Accepts:
      UploadFile OR file path
    """

    try:
        if hasattr(file_or_path, "file"):
            image = Image.open(
                file_or_path.file
            )

        else:
            image = Image.open(
                file_or_path
            )

        image = image.convert("RGB")

        return image

    except UnidentifiedImageError:
        raise ValueError(
            "Invalid or corrupted image"
        )


# =====================================================
# STANDARDIZATION
# =====================================================

def standardize_image(pil_image):
    """
    Convert image to canonical form:
    RGB
    224x224
    float32
    """

    img_resized = pil_image.resize(
        IMG_SIZE
    )

    img_np = np.asarray(
        img_resized,
        dtype=np.float32
    )

    return img_np


def add_batch_dimension(img_np):
    return np.expand_dims(
        img_np,
        axis=0
    )


# =====================================================
# MODEL-SPECIFIC PREPROCESS
# =====================================================

def preprocess_for_type_classifier(img_np):
    """
    MobileNetV2 preprocessing
    """
    batch = add_batch_dimension(img_np)

    return mobilenet_preprocess(
        batch.astype(np.float32)
    )


def preprocess_for_efficientnet(img_np):
    """
    Chest / Bone / Knee models
    """
    batch = add_batch_dimension(img_np)

    return efficientnet_preprocess(
        batch.astype(np.float32)
    )


def preprocess_patch_model(img_np):
    """
    Dental patch model uses MobileNetV2.
    """
    batch = add_batch_dimension(img_np)

    return mobilenet_preprocess(
        batch.astype(np.float32)
    )


# =====================================================
# MAIN PIPELINE
# =====================================================

def prepare_image(file_or_path) -> Dict[str, Any]:
    """
    Master preprocessing function.

    Returns:
    {
      pil_image,
      image_np,
      image_hash,
      tensors
    }
    """

    pil_image = load_pil_image(
        file_or_path
    )

    img_np = standardize_image(
        pil_image
    )

    if hasattr(file_or_path, "file"):
        file_or_path.file.seek(0)
        raw_bytes = file_or_path.file.read()
        file_or_path.file.seek(0)

        image_hash = compute_image_hash(
            raw_bytes
        )

    else:
        with open(file_or_path, "rb") as f:
            image_hash = compute_image_hash(
                f.read()
            )

    tensors = {
        "type_classifier":
            preprocess_for_type_classifier(
                img_np
            ),

        "efficientnet":
            preprocess_for_efficientnet(
                img_np
            )
    }

    return {
        "pil_image": pil_image,
        "image_np": img_np,
        "image_hash": image_hash,
        "tensors": tensors
    }


# =====================================================
# DENTAL SPECIAL PREP
# =====================================================

def prepare_dental_image(file_or_path):
    """
    Dental detector uses 512x512 image.
    """

    pil_image = load_pil_image(
        file_or_path
    )

    img = pil_image.resize(
        (512,512)
    )

    img_np = np.asarray(
        img,
        dtype=np.float32
    )

    return img_np


# =====================================================
# PATCH BATCH HELPER
# =====================================================

def batch_preprocess_patches(
    patches_np
):
    """
    Input:
       list/array of patches

    Output:
       batched preprocessed tensor
    """

    patches_np = np.asarray(
        patches_np,
        dtype=np.float32
    )

    return mobilenet_preprocess(
        patches_np
    )