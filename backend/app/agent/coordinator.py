"""
AGENT协调器
协调多个专业AGENT的协作流程
"""

import logging
from typing import Dict, Any, Optional
from app.agent.state import AgentState, create_initial_state
from app.agent.base import BaseAgent
from app.agent.recognition_agent.agent import RecognitionAgent
from app.agent.recommendation_agent.agent import SkillRecommendationAgent
from app.agent.intervention_agent.agent import InterventionAgent
from app.agent.message_bus import message_bus, MessageType, AgentMessage

logger = logging.getLogger(__name__)


class AgentCoordinator:
    """多AGENT协调器"""

    def __init__(self):
        self.recognition_agent = RecognitionAgent()
        self.skill_agent = SkillRecommendationAgent()
        self.intervention_agent = InterventionAgent()
        self.message_bus = message_bus

    async def process_conversation(
        self, user_input: str, state: AgentState
    ) -> Dict[str, Any]:
        """
        协调处理整个对话流程

        Args:
            user_input: 用户输入
            state: 当前状态

        Returns:
            处理结果和响应
        """
        try:
            updated_state = dict(state)
            updated_state["latest_message"] = user_input

            logger.info("===== 阶段1: 识别AGENT =====")
            updated_state = await self.recognition_agent.process(
                updated_state, user_input
            )

            if updated_state.get("emergency_detected"):
                logger.warning(f"检测到紧急情况: {updated_state.get('emergency_type')}")
                return {
                    "response": updated_state.get("emergency_response"),
                    "should_end": True,
                    "next_agent": None,
                    "state": updated_state,
                    "emergency_detected": True,
                }

            if updated_state.get("needs_clarification"):
                return {
                    "response": updated_state.get("clarification_prompt"),
                    "should_end": False,
                    "next_agent": "recognition",
                    "state": updated_state,
                    "identified_emotion": updated_state.get("identified_emotion"),
                }

            logger.info("===== 阶段2: 技能推荐AGENT =====")
            updated_state = await self.skill_agent.process(updated_state)

            if updated_state.get("is_crisis"):
                logger.warning("危机确认，需要干预")
                crisis_response = await self.intervention_agent.process(
                    updated_state, user_input
                )
                return {
                    "response": crisis_response.get(
                        "response", "我建议我们先停下来深呼吸一下。"
                    ),
                    "should_end": crisis_response.get("should_end", False),
                    "next_agent": "intervention"
                    if not crisis_response.get("should_end")
                    else None,
                    "is_crisis": True,
                    "state": updated_state,
                }

            logger.info("===== 阶段3: 干预引导AGENT =====")
            intervention_result = await self.intervention_agent.process(
                updated_state, user_input
            )

            return {
                "response": intervention_result.get("response", "我理解你的感受。"),
                "should_end": intervention_result.get("should_end", False),
                "next_agent": "intervention",
                "state": updated_state,
                "identified_emotion": updated_state.get("identified_emotion"),
                "recommended_skill": updated_state.get("recommended_skill"),
                "guidance_state": intervention_result.get("guidance_state"),
                "effectiveness": intervention_result.get("effectiveness"),
            }

        except Exception as e:
            logger.error(f"协调器处理失败: {str(e)}")
            return {
                "response": "抱歉，我现在不太舒服。请稍后再试。",
                "should_end": True,
                "error": str(e),
            }

    def _generate_recommendation_response(self, skill_info: Dict) -> str:
        """生成技能推荐响应"""
        if not skill_info:
            return "我建议您尝试一些放松的技巧，比如深呼吸。"

        skill_name = skill_info.get("name", "正念呼吸")
        introduction = skill_info.get("introduction", "")
        reason = skill_info.get("reason", "")
        estimated_duration = skill_info.get("estimated_duration", "5-10分钟")

        response = f"""根据您当前的状态，我为您推荐「{skill_name}」。

{introduction}

推荐理由：{reason}

预计用时：{estimated_duration}

您想尝试练习这个技能吗？"""

        return response

    def get_state_for_client(self, state: AgentState) -> Dict:
        """获取客户端需要的状态"""
        return {
            "identified_emotion": state.get("identified_emotion"),
            "emergency_detected": state.get("emergency_detected", False),
            "risk_level": state.get("risk_level", "low"),
            "recommended_skill": state.get("recommended_skill"),
            "guidance_state": state.get("guidance_state"),
        }


coordinator = AgentCoordinator()
