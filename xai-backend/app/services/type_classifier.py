"""
Type Classifier Service
-----------------------

Predicts X-ray modality:

- chest
- bone
- dental
- knee
"""

import numpy as np

from app.core.model_registry import (
    ModelRegistry,
    predict_single
)


class TypeClassifierService:

    @staticmethod
    def predict(
        prepared_image
    ):
        """
        Input:
          output of prepare_image()

        Returns:
        {
          type,
          confidence,
          probabilities
        }
        """

        model = ModelRegistry.get_type_classifier()

        tensor = prepared_image[
            "tensors"
        ]["type_classifier"]

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
            .get_type_labels()
        )

        predicted_type = idx_to_label[
            pred_idx
        ]

        probabilities = {
            idx_to_label[i]:
            float(preds[i])

            for i in range(
                len(preds)
            )
        }

        return {
            "type":
                predicted_type,

            "confidence":
                confidence,

            "probabilities":
                probabilities
        }

    @staticmethod
    def get_predicted_type(
        prepared_image
    ):
        """
        Convenience helper
        """

        result = (
            TypeClassifierService
            .predict(
                prepared_image
            )
        )

        return result["type"]