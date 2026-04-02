"""
识别AGENT模块
专注于用户输入分析和情绪识别
"""

from .agent import RecognitionAgent
from .prompts import RECOGNITION_AGENT_PROMPT
from .tools import CrisisDetector

__all__ = ["RecognitionAgent", "RECOGNITION_AGENT_PROMPT", "CrisisDetector"]
