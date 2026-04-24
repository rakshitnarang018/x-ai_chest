"""
Analyze Endpoint
----------------

POST /analyze
"""

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

from app.pipeline.orchestrator import (
    AnalysisOrchestrator
)

from app.schemas.response_models import (
    AnalyzeResponse
)


router = APIRouter()


@router.post(
    "/analyze",
    response_model=AnalyzeResponse
)
async def analyze_image(
    file: UploadFile = File(...)
):
    """
    Upload image for analysis.
    Immediate prediction response.
    """

    try:

        result = (
            AnalysisOrchestrator
            .analyze(
                file
            )
        )

        return result


    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        print(
          f"/analyze error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
             "Internal analysis error"
            )
        )