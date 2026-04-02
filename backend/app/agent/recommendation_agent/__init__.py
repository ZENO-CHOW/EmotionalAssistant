"""
技能推荐AGENT模块
专注于危机检测和DBT技能推荐
"""

from .agent import SkillRecommendationAgent
from .rules import SkillRecommendationRules
from .prompts import SKILL_RECOMMENDATION_PROMPT

__all__ = [
    "SkillRecommendationAgent",
    "SkillRecommendationRules",
    "SKILL_RECOMMENDATION_PROMPT",
]
