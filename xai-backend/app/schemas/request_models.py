"""
Request Schemas
---------------

Pydantic request models for API validation.
"""

from typing import Optional

from pydantic import (
    BaseModel,
    Field
)


# =====================================================
# ANALYSIS OPTIONS
# =====================================================

class AnalysisOptions(
    BaseModel
):
    """
    Optional flags for future extension.
    """

    generate_gradcam: bool = Field(
        default=True
    )

    generate_report: bool = Field(
        default=True
    )

    enable_lime: bool = Field(
        default=False
    )


# =====================================================
# LIME REQUEST
# =====================================================

class LimeRequest(
    BaseModel
):
    """
    Trigger on-demand LIME.
    """

    num_samples: Optional[int] = Field(
        default=None,
        ge=50,
        le=1000
    )


# =====================================================
# JOB LOOKUP
# =====================================================

class JobRequest(
    BaseModel
):
    job_id: str


# =====================================================
# HEALTH CHECK (placeholder)
# =====================================================

class HealthRequest(
    BaseModel
):
    ping: str = "ok"