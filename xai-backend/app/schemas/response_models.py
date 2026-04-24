"""
Response Schemas
----------------

Pydantic response contracts
"""

from typing import Dict, Optional, List

from pydantic import (
    BaseModel
)


# ======================================================
# DENTAL DETECTION BOX
# ======================================================

class DetectionBox(
    BaseModel):
    x:int
    y:int
    w:int
    h:int
    confidence:float


# ======================================================
# PREDICTION PAYLOAD
# ======================================================

class PredictionResponse(
    BaseModel):

    domain:str

    label:str

    confidence:float

    severity:str

    probabilities:Optional[
        Dict[str,float]
    ] = None

    detections:Optional[
        List[DetectionBox]
    ] = None

    num_detections:Optional[
        int
    ] = None


# ======================================================
# INITIAL ANALYZE RESPONSE
# ======================================================

class AnalyzeResponse(
    BaseModel):

    job_id:str

    scan_type:str

    type_confidence:float

    prediction:PredictionResponse

    status:Dict[
       str,
       str
    ]


# ======================================================
# REPORT PAYLOAD
# ======================================================

class ReportContent(
    BaseModel):
    findings:str
    impression:str
    limitations:str


class ReportResponse(
    BaseModel):

    model:str

    generated:bool

    report:ReportContent


# ======================================================
# XAI ARTIFACT
# ======================================================

class XAIArtifact(
    BaseModel):

    available:bool

    image_base64:Optional[
        str
    ]=None

    type:Optional[
       str
    ]=None

    reason:Optional[
       str
    ]=None


# ======================================================
# POLLING RESPONSE
# ======================================================

class AnalysisResultResponse(
    BaseModel):

    job_id:str

    prediction:PredictionResponse

    status:Dict[
      str,
      str
    ]

    gradcam:Optional[
      XAIArtifact
    ] = None

    report:Optional[
      ReportResponse
    ] = None

    lime:Optional[
      XAIArtifact
    ] = None


# ======================================================
# HEALTH
# ======================================================

class HealthResponse(
    BaseModel):

    status:str

    models_loaded:bool

    version:str