from fastapi import APIRouter, HTTPException, status, Depends
from app.models.schemas import (
    EvaluationRequest, EvaluationResponse, 
    HealthResponse, VersionResponse, ErrorResponse
)
from app.services.fit_engine import FitEngine
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

def get_fit_engine() -> FitEngine:
    """Dependency to get fit engine instance"""
    from main import fit_engine
    if fit_engine is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service not initialized"
        )
    return fit_engine

@router.post("/evaluate-fit", response_model=EvaluationResponse)
async def evaluate_fit(
    request: EvaluationRequest,
    engine: FitEngine = Depends(get_fit_engine)
):
    """Evaluate resume-job fit and generate learning recommendations"""
    try:
        result = await engine.evaluate_fit(request)
        logger.info(f"Evaluation completed with score: {result.fit_score}")
        return result
    except Exception as e:
        logger.error(f"Error in evaluate_fit: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to evaluate resume fit"
        )

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse()

@router.get("/version", response_model=VersionResponse)
async def get_version():
    """Get service version"""
    return VersionResponse()
