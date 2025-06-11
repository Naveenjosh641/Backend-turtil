import json
import logging
from typing import List, Dict
from app.models.schemas import LearningStep

logger = logging.getLogger(__name__)

class LearningPathGenerator:
    """Generate learning paths for missing skills"""
    
    def __init__(self, learning_paths_file: str, max_steps: int = 4):
        self.learning_paths_file = learning_paths_file
        self.max_steps = max_steps
        self.learning_paths: Dict = {}
    
    async def initialize(self):
        """Load learning paths configuration"""
        try:
            with open(self.learning_paths_file, 'r', encoding='utf-8') as f:
                self.learning_paths = json.load(f)
            
            logger.info(f"Loaded learning paths for {len(self.learning_paths)} skills")
            
        except Exception as e:
            logger.error(f"Failed to load learning paths: {e}")
            raise
    
    def generate_learning_track(self, missing_skills: List[str]) -> List[LearningStep]:
        """Generate learning track for missing skills"""
        learning_track = []
        
        for skill in missing_skills:
            skill_lower = skill.lower()
            
            # Try to find learning path
            learning_path = None
            if skill_lower in self.learning_paths:
                learning_path = self.learning_paths[skill_lower]
            else:
                # Try fuzzy matching
                for path_skill, path_data in self.learning_paths.items():
                    if skill_lower in path_skill or path_skill in skill_lower:
                        learning_path = path_data
                        break
            
            if learning_path:
                steps = learning_path.get('steps', [])[:self.max_steps]
                if steps:
                    learning_track.append(LearningStep(skill=skill, steps=steps))
            else:
                # Generate generic learning path
                generic_steps = [
                    f"Research {skill} fundamentals and core concepts",
                    f"Complete online tutorials or courses on {skill}",
                    f"Build a small project using {skill}",
                    f"Practice {skill} through hands-on exercises"
                ][:self.max_steps]
                
                learning_track.append(LearningStep(skill=skill, steps=generic_steps))
        
        return learning_track
