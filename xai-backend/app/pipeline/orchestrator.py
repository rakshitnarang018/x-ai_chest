"""
Analysis Orchestrator
---------------------

Master pipeline coordinator.
"""

from app.services.preprocessing import (
    validate_file_extension,
    validate_file_size,
    prepare_image
)

from app.services.router import (
    PredictionRouter
)

from app.core.job_store import (
    JobStore
)

from app.core.executor import (
    submit_enrichment_tasks
)

from app.xai.gradcam_service import (
    generate_gradcam
)

from app.llm.report_service import (
    generate_report
)

from app.pipeline.runtime_context import (
    RuntimeContext
)


class AnalysisOrchestrator:

    # ====================================================
    # MAIN ENTRYPOINT
    # ====================================================

    @staticmethod
    def analyze(
        upload_file
    ):
        """
        Main pipeline:
        validate
        preprocess
        predict
        create job
        store runtime context
        launch background tasks
        return immediately
        """

        # --------------------------------
        # Validate upload
        # --------------------------------

        validate_file_extension(
            upload_file.filename
        )

        validate_file_size(
            upload_file
        )


        # --------------------------------
        # Preprocess image
        # --------------------------------

        prepared_image = prepare_image(
            upload_file
        )

        upload_file.file.seek(0)


        # --------------------------------
        # Prediction routing
        # --------------------------------

        routed_result = (
            PredictionRouter
            .route_prediction(
                prepared_image,
                upload_file
            )
        )

        prediction_payload = (
            routed_result[
                "prediction"
            ]
        )


        # --------------------------------
        # Create analysis job
        # --------------------------------

        job_id = (
            JobStore.create_job(
                prediction_payload
            )
        )


        # --------------------------------
        # Store runtime context
        # Required later for deferred LIME
        # --------------------------------

        RuntimeContext.set(
            job_id,
            {
                "prepared_image":
                    prepared_image,

                "prediction":
                    prediction_payload
            }
        )


        # --------------------------------
        # Launch parallel enrichment
        # --------------------------------

        submit_enrichment_tasks(
            job_id=job_id,

            image_bundle=
                prepared_image,

            prediction_payload=
                prediction_payload,

            gradcam_fn=
                generate_gradcam,

            report_fn=
                generate_report
        )


        # --------------------------------
        # Immediate response
        # --------------------------------

        return {

            "job_id":
                job_id,

            "scan_type":
                routed_result[
                    "scan_type"
                ],

            "type_confidence":
                routed_result[
                    "type_confidence"
                ],

            "prediction":
                prediction_payload,

            "status":{
                "gradcam":
                    "queued",

                "report":
                    "queued",

                "lime":
                    "not_requested"
            }
        }



    # ====================================================
    # POLLING HELPER
    # ====================================================

    @staticmethod
    def get_analysis_result(
        job_id
    ):
        result = (
            JobStore
            .build_analysis_response(
                job_id
            )
        )

        if result is None:
            raise ValueError(
                "Job not found"
            )

        return result


    # ====================================================
    # OPTIONAL CLEANUP
    # (for future TTL cleanup)
    # ====================================================

    @staticmethod
    def clear_runtime_context(
        job_id
    ):
        RuntimeContext.delete(
            job_id
        )