"""
Knee Predictor Service
----------------------

Knee X-ray osteoporosis detection
"""

import numpy as np

from app.core.model_registry import (
    ModelRegistry,
    predict_single
)

from app.core.config import (
    get_severity_from_confidence
)


# =====================================================
# LABEL NORMALIZATION
# =====================================================

FRONTEND_LABELS = {
    "NORMAL": "Normal",
    "OSTEOPOROSIS": "Osteoporosis"
}


class KneePredictor:

    @staticmethod
    def predict(
        prepared_image
    ):
        """
        Input:
          output from prepare_image()

        Returns:
        {
          label
          confidence
          severity
          probabilities
        }
        """

        model = (
            ModelRegistry
            .get_knee_model()
        )

        tensor = prepared_image[
            "tensors"
        ]["efficientnet"]

        preds = predict_single(
            model,
            tensor
        )

        pred_idx = int(
            np.argmax(preds)
        )

        confidence = float(
            preds[pred_idx]
        )

        idx_to_label = (
            ModelRegistry
            .get_knee_labels()
        )

        raw_label = idx_to_label[
            pred_idx
        ]

        frontend_label = (
            FRONTEND_LABELS[
                raw_label
            ]
        )

        severity = (
            "none"
            if frontend_label=="Normal"
            else get_severity_from_confidence(
                confidence
            )
        )

        probabilities = {}

        for i,p in enumerate(preds):

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
            "domain":
                "knee",

            "label":
                frontend_label,

            "confidence":
                confidence,

            "severity":
                severity,

            "probabilities":
                probabilities
        }


    @staticmethod
    def predict_label_only(
        prepared_image
    ):
        result = (
            KneePredictor.predict(
                prepared_image
            )
        )

        return result["label"]