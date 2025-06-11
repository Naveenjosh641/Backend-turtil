import logging
import numpy as np
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import asyncio

logger = logging.getLogger(__name__)

class ScoringEngine:
    """Calculate similarity scores between resume and job description"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words='english',
            max_features=1000,
            ngram_range=(1, 2)
        )
    
    async def calculate_fit_score(self, resume_skills: List[str], job_skills: List[str]) -> Tuple[float, List[str], List[str]]:
        """Calculate fit score and identify matched/missing skills"""
        if not resume_skills or not job_skills:
            return 0.0, [], job_skills
        
        resume_skills_set = set(skill.lower() for skill in resume_skills)
        job_skills_set = set(skill.lower() for skill in job_skills)
        
        # Find matches
        matched_skills_lower = resume_skills_set.intersection(job_skills_set)
        matched_skills = [skill for skill in resume_skills if skill.lower() in matched_skills_lower]
        
        # Find missing skills
        missing_skills_lower = job_skills_set - resume_skills_set
        missing_skills = [skill for skill in job_skills if skill.lower() in missing_skills_lower]
        
        # Calculate score based on matched skills ratio
        if not job_skills:
            score = 1.0
        else:
            score = len(matched_skills_lower) / len(job_skills_set)
        
        return min(score, 1.0), matched_skills, missing_skills
    
    async def calculate_text_similarity(self, resume_text: str, job_text: str) -> float:
        """Calculate text similarity using TF-IDF and cosine similarity"""
        try:
            # Prepare texts
            texts = [resume_text, job_text]
            
            # Vectorize
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            
            # Calculate cosine similarity
            similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            
            return float(similarity_matrix[0][0])
            
        except Exception as e:
            logger.error(f"Error calculating text similarity: {e}")
            return 0.0
