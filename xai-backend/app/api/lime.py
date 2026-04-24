"""
LIME Endpoint
-------------

POST /analysis/{job_id}/lime
"""

from fastapi import (
    APIRouter,
    HTTPException
)

from app.core.job_store import (
    JobStore
)

from app.core.executor import (
    submit_lime_task
)

from app.xai.lime_service import (
    generate_lime
)

# temporary in-memory context bridge
# populated by orchestrator
from app.pipeline.runtime_context import (
    RuntimeContext
)


router = APIRouter()


@router.post(
    "/analysis/{job_id}/lime"
)
async def generate_lime_for_job(
    job_id:str
):
    """
    Trigger on-demand LIME generation.
    """

    if not JobStore.exists(
        job_id
    ):
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )


    job = JobStore.get_job(
        job_id
    )

    # Prevent duplicate LIME runs
    if job["status"]["lime"] in (
        "queued",
        "running",
        "done"
    ):
        return {
            "message":
               "LIME already requested",

            "status":
               job["status"]["lime"]
        }


    try:

        context = (
            RuntimeContext
            .get(job_id)
        )

        if context is None:
            raise HTTPException(
                status_code=404,
                detail=(
                  "Context expired "
                  "for LIME generation"
                )
            )


        submit_lime_task(
            job_id=job_id,

            lime_fn=generate_lime,

            prepared_image=
                context[
                  "prepared_image"
                ],

            prediction_payload=
                context[
                  "prediction"
                ]
        )


        return {

            "message":
                "LIME generation started",

            "status":
                "queued",

            "job_id":
                job_id
        }


    except HTTPException:
        raise

    except Exception as e:

        print(
          f"LIME endpoint error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
              "Failed to launch LIME"
            )
        )