"""
Dental Predictor Service
Final calibrated anomaly-based version
--------------------------------------

Whole image
-> patch extraction
-> patch scoring
-> cavity decision from anomaly patch score
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
    TOP_PATCH_RATIO
)

from app.services.preprocessing import (
    prepare_dental_image,
    batch_preprocess_patches
)


# ------------------------------------
# Tuned anomaly threshold
# ------------------------------------
DENTAL_ANOMALY_THRESHOLD = 0.58


# ======================================================
# PATCH EXTRACTION
# ======================================================

def extract_patches(
    image,
    patch_size=PATCH_SIZE,
    stride=PATCH_STRIDE
):
    patches=[]

    h,w,_=image.shape

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
            patch=image[
                y:y+patch_size,
                x:x+patch_size
            ]

            patches.append(
                (patch,x,y)
            )

    return patches


# ======================================================
# PATCH FILTER
# ======================================================

def is_valid_patch(
    patch
):
    gray=cv2.cvtColor(
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
# INFORMATIVE PATCH SELECTION
# ======================================================

def get_top_patches(
    patches,
    top_ratio=TOP_PATCH_RATIO
):
    scored=[]

    for patch,x,y in patches:

        gray=cv2.cvtColor(
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
# MODEL PATCH SCORING
# ======================================================

def score_patches(
    image_np
):
    model=(
        ModelRegistry
        .get_dental_model()
    )

    patches=extract_patches(
        image_np
    )

    patches=[
        p for p in patches
        if is_valid_patch(
            p[0]
        )
    ]

    patches=get_top_patches(
        patches
    )

    if len(patches)>64:
        patches=patches[:64]

    if len(patches)==0:
        return [], []

    patch_arrays=[]
    coordinates=[]

    for patch,x,y in patches:

        patch_arrays.append(
            patch
        )

        coordinates.append(
            (x,y)
        )

    batch_tensor=(
        batch_preprocess_patches(
            patch_arrays
        )
    )

    preds=predict(
        model,
        batch_tensor
    )

    scores=[
        float(p[0])
        for p in preds
    ]

    return scores,coordinates


# ======================================================
# ANOMALY DECISION
# ======================================================

def classify_from_scores(
    scores,
    coordinates
):

    if len(scores)==0:
        return (
            "Normal",
            0.95,
            []
        )

    min_score=min(scores)

    mean_score=float(
        np.mean(scores)
    )


    cavity_flag = (
        (min_score < 0.62)
        or
        (
            min_score < 0.69
            and mean_score < 0.73
        )
    )


    if cavity_flag:

        detections=[]

        for i,s in enumerate(scores):

            if s < 0.69:

                x,y=coordinates[i]

                detections.append(
                    {
                      "x":int(x),
                      "y":int(y),
                      "w":PATCH_SIZE,
                      "h":PATCH_SIZE,
                      "confidence":float(
                           1-s
                      )
                    }
                )

        return (
            "Cavity",
            float(1-min_score),
            detections
        )


    # =========================================
    # NORMAL CASE EXPLAINABILITY BOXES
    # Return top confidence patches as evidence
    # =========================================

    detections=[]

    top_indices=np.argsort(
        scores
    )[-3:]

    for i in top_indices:

        x,y=coordinates[i]

        detections.append(
            {
              "x":int(x),
              "y":int(y),
              "w":PATCH_SIZE,
              "h":PATCH_SIZE,
              "confidence":float(
                   scores[i]
              )
            }
        )

    return (
        "Normal",
        float(mean_score),
        detections
    )


# ======================================================
# MAIN PREDICTOR
# ======================================================

class DentalPredictor:

    @staticmethod
    def predict(
        image_input
    ):

        image_np=prepare_dental_image(
            image_input
        )

        scores,coordinates=(
            score_patches(
                image_np
            )
        )

        (
            label,
            confidence,
            detections
        )=classify_from_scores(
            scores,
            coordinates
        )

        return {

            "domain":"dental",

            "label":label,

            "confidence":
                float(
                    confidence
                ),

            "severity":
                (
                  "moderate"
                  if label=="Cavity"
                  else "none"
                ),

            "detections":
                detections,

            "num_detections":
                len(
                    detections
                )
        }