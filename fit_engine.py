import json
import logging
from typing import Tuple
from app.core.config import get_settings
from app.models.schemas import EvaluationRequest, EvaluationResponse, FitVerdict, LearningStep
from app.services.skill_extractor import SkillExtractor
from app.services.scoring_engine import ScoringEngine
from app.services.learning_path_generator import LearningPathGenerator

logger = logging.getLogger(__name__)

class FitEngine:
    """Main engine for evaluating resume-job fit"""
    
    def __init__(self):
        self.settings = get_settings()
        self.skill_extractor = SkillExtractor(self.settings.skills_file)
        self.scoring_engine = ScoringEngine()
        self.learning_path_generator = LearningPathGenerator(
            self.settings.learning_paths_file,
            self.settings.max_steps_per_skill
        )
        self.config_data = {}
    
    async def initialize(self):
        """Initialize all components"""
        try:
            # Load configuration
            with open(self.settings.config_file, 'r', encoding='utf-8') as f:
                self.config_data = json.load(f)
            
            # Initialize components
            await self.skill_extractor.initialize()
            await self.learning_path_generator.initialize()
            
            logger.info("FitEngine initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize FitEngine: {e}")
            raise
    
    async def evaluate_fit(self, request: EvaluationRequest) -> EvaluationResponse:
        """Evaluate resume-job fit and generate recommendations"""
        try:
            # Extract skills
            resume_skills = self.skill_extractor.extract_skills(request.resume_text)
            job_skills = self.skill_extractor.extract_skills(request.job_description)
            
            # Normalize skills
            resume_skills = self.skill_extractor.normalize_skills(resume_skills)
            job_skills = self.skill_extractor.normalize_skills(job_skills)
            
            # Calculate fit score
            skill_score, matched_skills, missing_skills = await self.scoring_engine.calculate_fit_score(
                resume_skills, job_skills
            )
            
            # Calculate text similarity for additional context
            text_similarity = await self.scoring_engine.calculate_text_similarity(
                request.resume_text, request.job_description
            )
            
            # Combine scores (weighted average)
            fit_score = (skill_score * 0.7) + (text_similarity * 0.3)
            
            # Determine verdict
            verdict = self._determine_verdict(fit_score)
            
            # Generate learning track only for non-strong fits
            learning_track = []
            if verdict != FitVerdict.STRONG_FIT and missing_skills:
                learning_track = self.learning_path_generator.generate_learning_track(missing_skills)
            
            return EvaluationResponse(
                fit_score=round(fit_score, 2),
                verdict=verdict,
                matched_skills=matched_skills,
                missing_skills=missing_skills,
                recommended_learning_track=learning_track
            )
            
        except Exception as e:
            logger.error(f"Error evaluating fit: {e}")
            raise
    
    def _determine_verdict(self, score: float) -> FitVerdict:
        """Determine fit verdict based on score"""
        if score >= self.settings.strong_fit_threshold:
            return FitVerdict.STRONG_FIT
        elif score >= self.settings.moderate_fit_threshold:
            return FitVerdict.MODERATE_FIT
        else:
            return FitVerdict.WEAK_FIT
