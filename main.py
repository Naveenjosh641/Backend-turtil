from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from contextlib import asynccontextmanager

from app.api.routes import router
from app.core.config import get_settings
from app.core.logging_config import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Global variable to store the fit engine
fit_engine = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global fit_engine
    try:
        logger.info("Starting Resume Fit Evaluator service...")
        from app.services.fit_engine import FitEngine
        fit_engine = FitEngine()
        await fit_engine.initialize()
        logger.info("Service initialized successfully")
        yield
    except Exception as e:
        logger.error(f"Failed to initialize service: {e}")
        raise
    finally:
        logger.info("Shutting down Resume Fit Evaluator service...")

def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    settings = get_settings()
    
    app = FastAPI(
        title="Resume-Role Fit Evaluator",
        description="AI-powered microservice for evaluating resume-job fit and generating learning paths",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(router, prefix="/api/v1")
    
    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        logger.error(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "error", "message": "Internal server error"}
        )
    
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
