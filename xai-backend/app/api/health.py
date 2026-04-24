"""
Health Endpoint
---------------

GET /health
"""

from fastapi import (
    APIRouter
)

from app.core.model_registry import (
    ModelRegistry
)

from app.core.config import (
    API_VERSION
)

from app.schemas.response_models import (
    HealthResponse
)


router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse
)
async def health_check():
    """
    Basic backend health.
    """

    try:

        loaded = (
            ModelRegistry
            .is_loaded()
        )

        return {

            "status":"ok",

            "models_loaded":
                loaded,

            "version":
                API_VERSION
        }

    except Exception:

        return {

            "status":"error",

            "models_loaded":
                False,

            "version":
                API_VERSION
        }