"""
技能推荐AGENT实现
专注于危机检测和DBT技能推荐
"""

import json
import logging
from typing import Dict, Any, Optional
from app.agent.base import BaseAgent
from app.agent.state import AgentState
from app.core.llm_client import get_llm_client
from app.agent.recommendation_agent.prompts import SKILL_RECOMMENDATION_PROMPT
from app.agent.recommendation_agent.rules import SkillRecommendationRules
from app.dbt.skills import SKILLS_DATABASE

logger = logging.getLogger(__name__)


class SkillRecommendationAgent(BaseAgent):
    """技能推荐AGENT"""

    AGENT_NAME = "skill_recommendation_agent"

    def __init__(self):
        self.llm = get_llm_client()
        self.rules = SkillRecommendationRules

    def get_system_prompt(self) -> str:
        """获取AGENT系统提示词"""
        return """你是一个专业的DBT技能推荐助手。你的任务是：

1. 根据用户情绪状态推荐合适的DBT技能
2. 生成个性化的推荐理由
3. 提供技能的温和介绍，让用户愿意尝试
4. 评估技能推荐的置信度

注意事项：
- 语气要温暖、支持性
- 推荐理由要具体、有说服力
- 不要强迫用户接受推荐
- 如果用户拒绝，提供替代方案"""

    async def process(
        self, state: Dict[str, Any], user_input: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        处理技能推荐

        Args:
            state: 当前状态
            user_input: 用户输入（可选）

        Returns:
            更新后的状态
        """
        try:
            identified_emotion = state.get("identified_emotion", {})
            emergency_detected = state.get("emergency_detected", False)

            if emergency_detected:
                return self._handle_crisis(state)

            emotion_type = identified_emotion.get("type", "calm")
            intensity = identified_emotion.get("intensity", 5)
            latest_message = user_input or state.get("latest_message", "")

            skill_result = await self._recommend_skill(
                emotion_type, intensity, latest_message
            )

            new_state = state.copy()
            new_state.update(
                {
                    "is_crisis": False,
                    "risk_level": "low",
                    "crisis_trigger": None,
                    "recommended_skill": skill_result.get("skill_info"),
                    "skill_confidence": skill_result.get("confidence", 0.7),
                    "current_agent": self.AGENT_NAME,
                }
            )

            logger.info(
                f"技能推荐AGENT完成: 推荐={skill_result.get('skill_name')}, "
                f"置信度={skill_result.get('confidence')}"
            )

            return new_state

        except Exception as e:
            logger.error(f"技能推荐AGENT处理失败: {str(e)}")
            return self._fallback_recommendation(state)

    def _handle_crisis(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """处理危机情况"""
        new_state = state.copy()
        new_state.update(
            {
                "is_crisis": True,
                "risk_level": state.get("risk_level", "high"),
                "crisis_trigger": state.get("emergency_type"),
                "recommended_skill": None,
                "skill_confidence": 0.0,
                "current_agent": self.AGENT_NAME,
            }
        )
        return new_state

    async def _recommend_skill(
        self, emotion_type: str, intensity: int, context: str = ""
    ) -> Dict[str, Any]:
        """
        推荐技能

        Args:
            emotion_type: 情绪类型
            intensity: 强度
            context: 上下文信息

        Returns:
            推荐结果
        """
        if not self.llm or not self.llm.client:
            return self._fallback_recommendation_logic(emotion_type, intensity)

        try:
            skills_info = self._format_skills_database()
            prompt = SKILL_RECOMMENDATION_PROMPT.format(
                emotion_type=emotion_type,
                intensity=intensity,
                user_message=context
                or f"用户当前情绪{emotion_type}，强度{intensity}/10",
                skills_database=skills_info,
            )

            messages = [{"role": "user", "content": prompt}]

            response = self.llm.chat(messages=messages, temperature=0.5)

            if response:
                skill_result = self._parse_skill_response(response)
                if skill_result:
                    return {
                        "skill_name": skill_result.get("skill_name"),
                        "skill_info": {
                            "name": skill_result.get("skill_name"),
                            "reason": skill_result.get("reason"),
                            "introduction": skill_result.get("introduction"),
                            "estimated_duration": skill_result.get(
                                "estimated_duration", "5-10分钟"
                            ),
                        },
                        "confidence": 0.85,
                    }

            return self._fallback_recommendation_logic(emotion_type, intensity)

        except Exception as e:
            logger.error(f"LLM技能推荐失败: {str(e)}")
            return self._fallback_recommendation_logic(emotion_type, intensity)

    def _format_skills_database(self) -> str:
        """格式化技能数据库为文本"""
        lines = []
        for skill_name, skill_data in SKILLS_DATABASE.items():
            introduction = skill_data.get("introduction", "")
            lines.append(f"- {skill_name}: {introduction}")
        return "\n".join(lines)

    def _parse_skill_response(self, response: str) -> Optional[Dict]:
        """解析技能推荐响应"""
        try:
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()

            result = json.loads(response)
            logger.info(f"技能推荐解析成功: {result}")
            return result
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {str(e)}")
            return None

    def _fallback_recommendation_logic(
        self, emotion_type: str, intensity: int
    ) -> Dict[str, Any]:
        """备用推荐逻辑（基于规则）"""
        recommended_skills = self.rules.get_recommended_skills(emotion_type, intensity)
        skill_name = recommended_skills[0] if recommended_skills else "正念呼吸"

        introduction = self.rules.get_skill_introduction(skill_name)
        estimated_duration = self._get_estimated_duration(skill_name)

        reason_map = {
            "anxiety": "这个技能可以帮助您平静下来，减少焦虑感",
            "anger": "这个技能可以帮助您释放愤怒，恢复平静",
            "sadness": "这个技能可以帮助您缓解悲伤情绪",
            "fear": "这个技能可以帮助您减少恐惧感",
            "joy": "这个技能可以帮助您更好地享受当下的快乐",
            "calm": "这个技能可以帮助您保持内心的平静",
        }

        return {
            "skill_name": skill_name,
            "skill_info": {
                "name": skill_name,
                "reason": reason_map.get(
                    emotion_type, "这个技能对您当前的状态会有帮助"
                ),
                "introduction": introduction,
                "estimated_duration": estimated_duration,
            },
            "confidence": 0.7,
        }

    def _fallback_recommendation(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """备用推荐（当出错时）"""
        new_state = state.copy()
        new_state.update(
            {
                "is_crisis": False,
                "risk_level": "low",
                "crisis_trigger": None,
                "recommended_skill": {
                    "name": "正念呼吸",
                    "reason": "这是最基础的放松技能",
                    "introduction": "通过专注于呼吸来稳定情绪",
                    "estimated_duration": "5分钟",
                },
                "skill_confidence": 0.5,
                "current_agent": self.AGENT_NAME,
            }
        )
        return new_state

    def _get_estimated_duration(self, skill_name: str) -> str:
        """获取预计时长"""
        duration_map = {
            "TIPP": "10-15分钟",
            "STOP": "2-3分钟",
            "正念呼吸": "5-10分钟",
            "正念观察": "5-10分钟",
            "情绪命名": "3-5分钟",
            "接地技术": "2-5分钟",
            "感恩练习": "5-10分钟",
        }
        return duration_map.get(skill_name, "5-10分钟")
