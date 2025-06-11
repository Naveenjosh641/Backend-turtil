from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional
from enum import Enum

class FitVerdict(str, Enum):
    STRONG_FIT = "strong_fit"
    MODERATE_FIT = "moderate_fit"
    WEAK_FIT = "weak_fit"

class EvaluationRequest(BaseModel):
    resume_text: str = Field(..., min_length=10, description="Resume content as text")
    job_description: str = Field(..., min_length=10, description="Job description text")
    
    @validator('resume_text', 'job_description')
    def validate_text_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Text cannot be empty or whitespace only")
        return v.strip()

class LearningStep(BaseModel):
    skill: str
    steps: List[str]

class EvaluationResponse(BaseModel):
    fit_score: float = Field(..., ge=0.0, le=1.0)
    verdict: FitVerdict
    matched_skills: List[str]
    missing_skills: List[str]
    recommended_learning_track: List[LearningStep]
    status: str = "success"

class HealthResponse(BaseModel):
    status: str = "ok"

class VersionResponse(BaseModel):
    model_version: str = "1.0.0"

class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
    details: Optional[Dict] = None
