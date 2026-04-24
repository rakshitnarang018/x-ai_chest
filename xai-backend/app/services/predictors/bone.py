"""
Bone Predictor Service
----------------------
Binary fracture detection
"""

import numpy as np

from app.core.model_registry import (
    ModelRegistry,
    predict_single
)

from app.core.config import (
    get_severity_from_confidence
)


FRONTEND_LABELS = {
    "FRACTURE": "Fracture",
    "NORMAL": "Normal"
}


class BonePredictor:

    @staticmethod
    def predict(prepared_image):

        model = ModelRegistry.get_bone_model()

        tensor = prepared_image["tensors"]["efficientnet"]

        preds = predict_single(
            model,
            tensor
        )

        # ----------------------------------
        # Case 1: Binary sigmoid output
        # Example: [0.83]
        # ----------------------------------
        if np.size(preds) == 1:

            prob_fracture = float(
                np.squeeze(preds)
            )

            if prob_fracture >= 0.5:
                label = "Fracture"
                confidence = prob_fracture

                severity = (
                    get_severity_from_confidence(
                        confidence
                    )
                )

            else:
                label = "Normal"
                confidence = 1 - prob_fracture
                severity = "none"

            probabilities = {
                "Fracture": prob_fracture,
                "Normal": 1 - prob_fracture
            }

        # ----------------------------------
        # Case 2: Two-class softmax output
        # Example: [0.2, 0.8]
        # ----------------------------------
        else:

            pred_idx = int(
                np.argmax(preds)
            )

            confidence = float(
                preds[pred_idx]
            )

            idx_to_label = (
                ModelRegistry
                .get_bone_labels()
            )

            raw_label = idx_to_label[
                pred_idx
            ]

            label = FRONTEND_LABELS[
                raw_label
            ]

            severity = (
                "none"
                if label == "Normal"
                else get_severity_from_confidence(
                    confidence
                )
            )

            probabilities = {}

            for i, p in enumerate(preds):

                raw_cls = idx_to_label[i]

                frontend_cls = (
                    FRONTEND_LABELS[
                        raw_cls
                    ]
                )

                probabilities[
                    frontend_cls
                ] = float(p)

        return {
            "domain": "bone",
            "label": label,
            "confidence": confidence,
            "severity": severity,
            "probabilities": probabilities
        }


    @staticmethod
    def predict_label_only(
        prepared_image
    ):
        return BonePredictor.predict(
            prepared_image
        )["label"]