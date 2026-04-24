"""
Dental Predictor Service
------------------------

Patch-based cavity detection

Pipeline:
512x512 image
-> extract patches
-> filter low-detail patches
-> select informative patches
-> batch predict patches
-> return cavity detections
"""

import cv2
import numpy as np

from app.core.model_registry import (
    ModelRegistry,
    predict
)

from app.core.config import (
    PATCH_SIZE,
    PATCH_STRIDE,
    PATCH_STD_THRESHOLD,
    TOP_PATCH_RATIO,
    DENTAL_DETECTION_THRESHOLD
)

from app.services.preprocessing import (
    prepare_dental_image,
    batch_preprocess_patches
)


# ======================================================
# PATCH EXTRACTION
# ======================================================

def extract_patches(
    image,
    patch_size=PATCH_SIZE,
    stride=PATCH_STRIDE
):
    patches = []

    h,w,_ = image.shape

    for y in range(
        0,
        h-patch_size+1,
        stride
    ):
        for x in range(
            0,
            w-patch_size+1,
            stride
        ):
            patch = image[
                y:y+patch_size,
                x:x+patch_size
            ]

            patches.append(
                (patch,x,y)
            )

    return patches


# ======================================================
# VALID PATCH FILTER
# ======================================================

def is_valid_patch(
    patch
):
    gray = cv2.cvtColor(
        patch.astype(
            np.uint8
        ),
        cv2.COLOR_RGB2GRAY
    )

    return (
        np.std(gray)
        > PATCH_STD_THRESHOLD
    )


# ======================================================
# TOP INFORMATIVE PATCHES
# ======================================================

def get_top_patches(
    patches,
    top_ratio=TOP_PATCH_RATIO
):
    scored=[]

    for patch,x,y in patches:

        gray = cv2.cvtColor(
            patch.astype(np.uint8),
            cv2.COLOR_RGB2GRAY
        )

        score=np.std(gray)

        scored.append(
            (
             score,
             patch,
             x,
             y
            )
        )

    scored.sort(
        reverse=True,
        key=lambda x:x[0]
    )

    k=max(
       1,
       int(
         len(scored)*top_ratio
       )
    )

    selected=scored[:k]

    return [
        (p,x,y)
        for _,p,x,y in selected
    ]


# ======================================================
# BATCH PATCH PREDICTION
# ======================================================

def detect_cavities(
    image_np
):
    model = (
        ModelRegistry
        .get_dental_model()
    )

    patches = extract_patches(
        image_np
    )

    patches = [
        p for p in patches
        if is_valid_patch(
           p[0]
        )
    ]

    patches = get_top_patches(
        patches
    )

    if len(patches)==0:
        return []

    patch_arrays=[]
    coordinates=[]

    for patch,x,y in patches:

        patch_arrays.append(
            patch
        )

        coordinates.append(
            (x,y)
        )

    batch_tensor = (
        batch_preprocess_patches(
            patch_arrays
        )
    )

    preds = predict(
        model,
        batch_tensor
    )

    detections=[]

    for i,p in enumerate(preds):

        score=float(
           p[0]
        )

        if score > DENTAL_DETECTION_THRESHOLD:

            x,y = coordinates[i]

            detections.append(
                {
                  "x":int(x),
                  "y":int(y),
                  "w":PATCH_SIZE,
                  "h":PATCH_SIZE,
                  "confidence":score
                }
            )

    return detections


# ======================================================
# MAIN PREDICTOR
# ======================================================

class DentalPredictor:

    @staticmethod
    def predict(
        image_input
    ):
        """
        Input:
           file path or upload

        Returns:
          dental detection response
        """

        image_np = prepare_dental_image(
            image_input
        )

        detections = detect_cavities(
            image_np
        )

        if len(detections)>0:

            max_conf=max(
              d["confidence"]
              for d in detections
            )

            label="Cavity"

        else:

            max_conf=0.95
            label="Normal"

        return {

            "domain":"dental",

            "label":label,

            "confidence":
                float(max_conf),

            "severity":
                (
                 "moderate"
                 if label=="Cavity"
                 else "none"
                ),

            "detections":
                detections,

            "num_detections":
                len(detections)
        }