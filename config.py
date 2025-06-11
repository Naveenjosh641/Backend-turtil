from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    """Application settings"""
    app_name: str = "Resume-Role Fit Evaluator"
    version: str = "1.0.0"
    debug: bool = False
    
    # File paths
    skills_file: str = "data/skills.json"
    learning_paths_file: str = "data/learning_paths.json"
    config_file: str = "data/config.json"
    
    # Model settings
    similarity_model: str = "tfidf"  # or "sentence_embeddings"
    max_steps_per_skill: int = 4
    
    # Fit score thresholds
    strong_fit_threshold: float = 0.7
    moderate_fit_threshold: float = 0.4
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

# app/core/logging_config.py
import logging
import sys
from pathlib import Path

def setup_logging():
    """Configure application logging"""
    # Create logs directory if it doesn't exist
    Path("logs").mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/app.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
