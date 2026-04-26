"""
Jobs / Polling Endpoint
-----------------------
GET /analysis/{job_id}
"""

from fastapi import (
    APIRouter,
    HTTPException
)

from app.pipeline.orchestrator import (
    AnalysisOrchestrator
)

from app.schemas.response_models import (
    AnalysisResultResponse
)


router = APIRouter()


@router.get(
    "/analysis/{job_id}",
    response_model=AnalysisResultResponse
)
async def get_analysis_job(
    job_id:str
):
    """
    Poll analysis results.
    """

    try:

        result = (
            AnalysisOrchestrator
            .get_analysis_result(
                job_id
            )
        )

        return result


    except ValueError:

        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )


    except Exception as e:

        print(
          f"/analysis error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
               "Could not fetch job"
            )
        )