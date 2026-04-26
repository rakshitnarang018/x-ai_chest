"""
Prediction Router
-----------------

Universal routing layer:

image
↓
type classifier
↓
correct predictor
"""

from app.services.type_classifier import (
    TypeClassifierService
)

from app.services.predictors.chest import (
    ChestPredictor
)

from app.services.predictors.bone import (
    BonePredictor
)

from app.services.predictors.knee import (
    KneePredictor
)

from app.services.predictors.dental import (
    DentalPredictor
)


class PredictionRouter:

    # ==========================================
    # ROUTE BY MODALITY
    # ==========================================

    @staticmethod
    def route_prediction(
        prepared_image,
        original_input
    ):
        """
        Main universal routing entry.

        Inputs:
            prepared_image:
               output of prepare_image()

            original_input:
               raw uploaded image/path
               needed for dental pipeline

        Returns:
            {
              scan_type,
              type_confidence,
              prediction
            }
        """

        type_result = (
            TypeClassifierService
            .predict(
                prepared_image
            )
        )

        scan_type = (
            type_result["type"]
        )

        if scan_type=="chest":

            prediction = (
                ChestPredictor
                .predict(
                    prepared_image
                )
            )

        elif scan_type=="bone":

            prediction = (
                BonePredictor
                .predict(
                    prepared_image
                )
            )

        elif scan_type=="knee":

            prediction = (
                KneePredictor
                .predict(
                    prepared_image
                )
            )

        elif scan_type=="dental":

            # special branch
            prediction = (
                DentalPredictor
                .predict(
                    original_input
                )
            )

        else:
            raise ValueError(
              f"Unsupported scan type: "
              f"{scan_type}"
            )

        return {

            "scan_type":
                scan_type,

            "type_confidence":
                type_result[
                    "confidence"
                ],

            "type_probabilities":
                type_result[
                    "probabilities"
                ],

            "prediction":
                prediction
        }


    # ==========================================
    # Convenience helper
    # ==========================================

    @staticmethod
    def detect_scan_type(
        prepared_image
    ):
        return (
            TypeClassifierService
            .predict(
                prepared_image
            )
        )