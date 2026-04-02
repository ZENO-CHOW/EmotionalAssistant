"""
识别AGENT实现
专注于用户输入分析和情绪识别
"""

import json
import logging
from typing import Dict, Any, Optional
from app.agent.base import BaseAgent
from app.agent.state import AgentState
from app.core.llm_client import get_llm_client
from app.agent.recognition_agent.prompts import (
    RECOGNITION_AGENT_PROMPT,
    EMOTION_ANALYSIS_SYSTEM_PROMPT,
)
from app.agent.recognition_agent.tools import CrisisDetector

logger = logging.getLogger(__name__)


class RecognitionAgent(BaseAgent):
    """识别AGENT"""

    AGENT_NAME = "recognition_agent"

    def __init__(self):
        self.llm = get_llm_client()
        self.crisis_detector = CrisisDetector()

    def get_system_prompt(self) -> str:
        """获取AGENT系统提示词"""
        return RECOGNITION_AGENT_PROMPT

    async def process(
        self, state: Dict[str, Any], user_input: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        处理用户输入，识别情绪和意图

        Args:
            state: 当前状态
            user_input: 用户输入文本

        Returns:
            更新后的状态
        """
        try:
            latest_message = user_input or state.get("latest_message", "")
            if not latest_message:
                logger.warning("识别AGENT: 没有用户输入")
                return state

            history = self._load_history(state)

            emotion_result = await self._analyze_emotion(latest_message, history)

            emergency_result = self.crisis_detector.detect_emergency(
                latest_message, emotion_result.get("intensity")
            )

            new_state = state.copy()
            new_state.update(
                {
                    "identified_emotion": {
                        "type": emotion_result.get("emotion_type"),
                        "intensity": emotion_result.get("intensity"),
                        "confidence": emotion_result.get("confidence"),
                        "reason": emotion_result.get("reason"),
                    },
                    "user_intention": emotion_result.get(
                        "user_intention", "casual_talk"
                    ),
                    "emergency_detected": emergency_result["detected"],
                    "emergency_type": emergency_result["type"],
                    "emergency_response": emergency_result.get("response"),
                    "emergency_keywords": emergency_result.get("matched_keywords", []),
                    "risk_level": emergency_result.get("risk_level", "low"),
                    "needs_clarification": emotion_result.get(
                        "needs_clarification", False
                    ),
                    "clarification_prompt": emotion_result.get("clarification_prompt"),
                    "current_agent": self.AGENT_NAME,
                }
            )

            logger.info(
                f"识别AGENT完成: 情绪={emotion_result.get('emotion_type')}, "
                f"紧急={emergency_result['detected']}"
            )

            return new_state

        except Exception as e:
            logger.error(f"识别AGENT处理失败: {str(e)}")
            new_state = state.copy()
            new_state.update(
                {
                    "identified_emotion": None,
                    "emergency_detected": False,
                    "current_agent": self.AGENT_NAME,
                }
            )
            return new_state

    async def _analyze_emotion(self, message: str, history: list) -> Dict[str, Any]:
        """
        使用LLM分析情绪

        Args:
            message: 用户消息
            history: 对话历史

        Returns:
            情绪分析结果
        """
        if not self.llm or not self.llm.client:
            return self._fallback_emotion_analysis(message)

        try:
            full_messages = []

            for msg in history:
                if msg.get("role") and msg.get("content"):
                    full_messages.append(
                        {"role": msg["role"], "content": msg["content"]}
                    )

            full_messages.append({"role": "user", "content": message})

            logger.info(f"传递对话历史，共 {len(history)} 条消息到LLM进行情绪分析")

            response = self.llm.chat(
                messages=full_messages,
                system_prompt=EMOTION_ANALYSIS_SYSTEM_PROMPT,
                temperature=0.3,
            )

            if response:
                result = self._parse_json_response(response)
                if result:
                    return result

            return self._fallback_emotion_analysis(message)

        except Exception as e:
            logger.error(f"LLM情绪分析失败: {str(e)}")
            return self._fallback_emotion_analysis(message)

    def _parse_json_response(self, response: str) -> Optional[Dict]:
        """解析JSON响应"""
        try:
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()

            result = json.loads(response)
            logger.info(f"情绪解析成功: {result}")
            return result
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {str(e)}")
            return None

    def _fallback_emotion_analysis(self, message: str) -> Dict[str, Any]:
        """
        备用情绪分析（基于关键词）

        Args:
            message: 用户消息

        Returns:
            情绪分析结果
        """
        message_lower = message.lower()

        emotion_keywords = {
            "joy": ["开心", "高兴", "快乐", "兴奋", "愉快", "幸福", "开心"],
            "calm": ["平静", "平静", "放松", "安心", "宁静"],
            "sadness": ["悲伤", "难过", "伤心", "失落", "沮丧", "抑郁"],
            "anxiety": ["焦虑", "担心", "紧张", "不安", "害怕", "恐惧"],
            "anger": ["愤怒", "生气", "烦躁", "恼火", "不满"],
            "fear": ["害怕", "恐惧", "惊恐", "担忧"],
        }

        emotion_type = "calm"
        max_matches = 0

        for emotion, keywords in emotion_keywords.items():
            matches = sum(1 for kw in keywords if kw in message)
            if matches > max_matches:
                max_matches = matches
                emotion_type = emotion

        intensity = self._estimate_intensity(message)

        return {
            "emotion_type": emotion_type,
            "intensity": intensity or 5,
            "confidence": 0.5,
            "reason": f"基于关键词分析检测到{emotion_type}情绪",
            "user_intention": "casual_talk",
            "needs_clarification": False,
            "clarification_prompt": None,
        }

    def _estimate_intensity(self, message: str) -> Optional[int]:
        """估计情绪强度"""
        message_lower = message.lower()

        high_intensity_words = [
            "非常",
            "极其",
            "极度",
            "特别",
            "受不了",
            "撑不住",
            "要崩溃",
        ]
        medium_intensity_words = ["比较", "有些", "相当", "让我烦恼"]
        low_intensity_words = ["有点", "稍微", "一般", "还好"]

        for word in high_intensity_words:
            if word in message_lower:
                return 8
        for word in medium_intensity_words:
            if word in message_lower:
                return 5
        for word in low_intensity_words:
            if word in message_lower:
                return 3

        return None
