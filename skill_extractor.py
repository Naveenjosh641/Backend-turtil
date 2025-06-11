import json
import re
import logging
from typing import List, Set, Dict
from pathlib import Path
import asyncio

logger = logging.getLogger(__name__)

class SkillExtractor:
    """Extract and normalize skills from text"""
    
    def __init__(self, skills_file: str):
        self.skills_file = skills_file
        self.skills_data: Dict = {}
        self.skill_aliases: Dict[str, str] = {}
        self.all_skills: Set[str] = set()
    
    async def initialize(self):
        """Load skills configuration"""
        try:
            with open(self.skills_file, 'r', encoding='utf-8') as f:
                self.skills_data = json.load(f)
            
            # Build skill aliases map
            for category, skills in self.skills_data.get('categories', {}).items():
                for skill_info in skills:
                    if isinstance(skill_info, dict):
                        main_skill = skill_info['name']
                        self.all_skills.add(main_skill.lower())
                        
                        # Add aliases
                        for alias in skill_info.get('aliases', []):
                            self.skill_aliases[alias.lower()] = main_skill
                    else:
                        # Simple string skill
                        self.all_skills.add(skill_info.lower())
            
            # Add direct aliases from config
            for alias, main_skill in self.skills_data.get('aliases', {}).items():
                self.skill_aliases[alias.lower()] = main_skill
            
            logger.info(f"Loaded {len(self.all_skills)} skills and {len(self.skill_aliases)} aliases")
            
        except Exception as e:
            logger.error(f"Failed to load skills data: {e}")
            raise
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from text"""
        if not text:
            return []
        
        text_lower = text.lower()
        found_skills = set()
        
        # Direct skill matching
        for skill in self.all_skills:
            if self._skill_in_text(skill, text_lower):
                found_skills.add(skill.title())
        
        # Alias matching
        for alias, main_skill in self.skill_aliases.items():
            if self._skill_in_text(alias, text_lower):
                found_skills.add(main_skill)
        
        return list(found_skills)
    
    def _skill_in_text(self, skill: str, text: str) -> bool:
        """Check if skill exists in text with word boundaries"""
        # Create pattern with word boundaries
        pattern = r'\b' + re.escape(skill) + r'\b'
        return bool(re.search(pattern, text, re.IGNORECASE))
    
    def normalize_skills(self, skills: List[str]) -> List[str]:
        """Normalize skill names using aliases"""
        normalized = []
        for skill in skills:
            skill_lower = skill.lower()
            if skill_lower in self.skill_aliases:
                normalized.append(self.skill_aliases[skill_lower])
            else:
                normalized.append(skill.title())
        return list(set(normalized))
