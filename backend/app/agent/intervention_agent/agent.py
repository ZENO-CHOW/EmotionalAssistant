"""
干预引导AGENT实现
专注于技能引导、效果评估和对话总结
"""

from typing import Dict, Any, Optional
import json
from app.agent.base import BaseAgent
from app.agent.intervention_agent.crisis_rules import (
    get_crisis_response,
    format_crisis_response,
)
from app.agent.intervention_agent.guidance import (
    SkillGuidance,
    GuidanceState,
    generate_skill_confirmation_message,
    get_alternative_skills,
)
from app.agent.intervention_agent.prompts import (
    INTERVENTION_AGENT_PROMPT,
    EFFECTIVENESS_EVALUATION_PROMPT,
    SESSION_SUMMARY_PROMPT,
    FOLLOW_UP_PROMPT,
    NEXT_STEP_PROMPT,
    CLOSING_PROMPT,
    EVALUATION_REQUEST_PROMPT,
)
from app.dbt.skills import SKILLS_DATABASE


class InterventionAgent(BaseAgent):
    """干预引导AGENT"""

    AGENT_NAME = "intervention_agent"

    def __init__(self):
        self.guidance = SkillGuidance()

    def get_system_prompt(self) -> str:
        """获取AGENT系统提示词"""
        return INTERVENTION_AGENT_PROMPT

    async def process(
        self, state: Dict[str, Any], user_input: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        处理输入，返回更新后的状态

        Args:
            state: 当前状态
            user_input: 用户输入（可选）

        Returns:
            更新后的状态
        """
        try:
            is_crisis = state.get("is_crisis", False)
            recommended_skill = state.get("recommended_skill")
            before_intensity = state.get("before_intensity") or state.get("intensity")
            next_action = state.get("next_action")

            if is_crisis:
                return await self._handle_crisis(state)

            if recommended_skill and next_action == "wait_skill_confirmation":
                return await self._handle_skill_confirmation(state, user_input)

            if self.guidance.state != GuidanceState.WAITING_CONFIRMATION:
                if user_input:
                    return await self._handle_guidance_step(state, user_input)

            if next_action == "wait_step_completion":
                if user_input:
                    return await self._handle_guidance_step(state, user_input)
                return self._request_step_input(state)

            if next_action == "wait_evaluation":
                return self._request_evaluation(state)

            if next_action == "wait_evaluation_result" and user_input:
                return await self._handle_evaluation(state, user_input)

            if next_action == "wait_summary":
                return await self._generate_summary(state)

            if next_action == "wait_closing":
                return self._generate_closing(state)

            return self._default_response(state)

        except Exception as e:
            return {
                "response": "抱歉，我现在不太舒服。请稍后再试。",
                "should_end": True,
                "error": str(e),
            }

    async def _handle_crisis(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """处理危机情况"""
        crisis_trigger = state.get("crisis_trigger") or "unknown"
        matched_keywords = state.get("matched_keywords", [])
        intensity = state.get("intensity")

        crisis_response = get_crisis_response(
            crisis_type=crisis_trigger,
            intensity=intensity,
            matched_keywords=matched_keywords,
        )

        response_text = format_crisis_response(crisis_response)

        return {
            "response": response_text,
            "response_type": "crisis_response",
            "should_end": crisis_response.get("should_end", True),
            "current_agent": self.AGENT_NAME,
            "next_action": "session_end"
            if crisis_response.get("should_end")
            else "continue",
        }

    async def _handle_skill_confirmation(
        self, state: Dict[str, Any], user_input: Optional[str]
    ) -> Dict[str, Any]:
        """处理技能确认"""
        recommended_skill = state.get("recommended_skill") or {}

        if not user_input:
            confirmation_msg = generate_skill_confirmation_message(recommended_skill)
            return {
                "response": confirmation_msg,
                "response_type": "skill_confirmation",
                "should_end": False,
                "current_agent": self.AGENT_NAME,
                "next_action": "wait_skill_confirmation",
                "recommended_skill": recommended_skill,
            }

        user_input_lower = user_input.lower()
        affirmative = any(
            word in user_input_lower
            for word in ["好", "愿意", "可以", "试试", "yes", "好的", "行"]
        )
        negative = any(
            word in user_input_lower
            for word in ["不", "不要", "不想", "no", "算", "不了"]
        )

        if negative or not affirmative:
            self.guidance.state = GuidanceState.DECLINED
            return {
                "response": "没关系。如果你改变主意，随时可以尝试。",
                "response_type": "skill_declined",
                "should_end": False,
                "current_agent": self.AGENT_NAME,
                "next_action": "wait_alternative_or_end",
            }

        self.guidance.initialize_guidance(recommended_skill)
        return self._get_first_step_response(recommended_skill)

    def _get_first_step_response(self, skill_data: Dict[str, Any]) -> Dict[str, Any]:
        """获取第一步引导响应"""
        steps = skill_data.get("steps", [])
        first_step = steps[0] if steps else {}

        return {
            "response": f"太好了！我们开始练习「{skill_data.get('name', '')}」。\n\n"
            f"**步骤 1/{len(steps)}**：{first_step.get('title', '')}\n\n"
            f"{first_step.get('description', '')}\n\n"
            f"请按以下指导进行：\n{first_step.get('guidance', '')}\n\n"
            f"准备好了吗？完成后告诉我你的感受。",
            "response_type": "guidance",
            "guidance_state": {
                "current_step": 1,
                "total_steps": len(steps),
                "completed": False,
                "waiting_for_input": True,
            },
            "should_end": False,
            "current_agent": self.AGENT_NAME,
            "next_action": "wait_step_completion",
            "skill_data": skill_data,
        }

    def _request_step_input(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """请求用户输入下一步"""
        skill_data = state.get("skill_data", {})
        steps = skill_data.get("steps", [])
        current_step = state.get("current_step", 1)
        first_step = steps[0] if steps else {}

        return {
            "response": f"**步骤 {current_step}/{len(steps)}**：{first_step.get('title', '')}\n\n"
            f"{first_step.get('description', '')}\n\n"
            f"请按以下指导进行：\n{first_step.get('guidance', '')}\n\n"
            f"完成后告诉我你的感受。",
            "response_type": "guidance",
            "guidance_state": {
                "current_step": current_step,
                "total_steps": len(steps),
                "completed": False,
                "waiting_for_input": True,
            },
            "should_end": False,
            "current_agent": self.AGENT_NAME,
            "next_action": "wait_step_completion",
        }

    async def _handle_guidance_step(
        self, state: Dict[str, Any], user_input: str
    ) -> Dict[str, Any]:
        """处理技能步骤响应"""
        skill_data = state.get("skill_data", {})
        steps = skill_data.get("steps", [])
        current_step = state.get("current_step", 1)

        if current_step < len(steps):
            next_step = current_step + 1
            step_data = steps[next_step - 1]
            return {
                "response": f"很好！继续努力。\n\n"
                f"**步骤 {next_step}/{len(steps)}**：{step_data.get('title', '')}\n\n"
                f"{step_data.get('description', '')}\n\n"
                f"请按以下指导进行：\n{step_data.get('guidance', '')}\n\n"
                f"完成后告诉我你的感受。",
                "response_type": "guidance",
                "guidance_state": {
                    "current_step": next_step,
                    "total_steps": len(steps),
                    "completed": False,
                    "waiting_for_input": True,
                },
                "should_end": False,
                "current_agent": self.AGENT_NAME,
                "next_action": "wait_step_completion",
                "skill_data": skill_data,
                "current_step": next_step,
            }
        else:
            return self._request_evaluation(state)

    def _request_evaluation(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """请求效果评估"""
        return {
            "response": EVALUATION_REQUEST_PROMPT,
            "response_type": "evaluation_request",
            "should_end": False,
            "current_agent": self.AGENT_NAME,
            "next_action": "wait_evaluation_result",
            "before_intensity": state.get("intensity"),
        }

    async def _handle_evaluation(
        self, state: Dict[str, Any], user_input: str
    ) -> Dict[str, Any]:
        """处理效果评估结果"""
        try:
            after_intensity = int(user_input)
        except (ValueError, TypeError):
            return {
                "response": "请告诉我一个数字（1-10），表示你现在的情绪强度。",
                "response_type": "evaluation_retry",
                "should_end": False,
                "current_agent": self.AGENT_NAME,
                "next_action": "wait_evaluation_result",
                "before_intensity": state.get("before_intensity"),
            }

        before_intensity = state.get("before_intensity") or state.get("intensity") or 5
        improvement = before_intensity - after_intensity

        if improvement >= 2:
            effectiveness = "有效"
        elif improvement >= -1:
            effectiveness = "一般"
        else:
            effectiveness = "无效"

        emotion_type = state.get("current_emotion", {}).get("type", "anxiety")

        if effectiveness == "有效":
            next_suggestion = "继续学习"
            next_skill = self._get_next_skill(emotion_type)
            advice = f"这个技能对你很有帮助！我们可以继续学习「{next_skill}」。"
        elif effectiveness == "一般":
            next_suggestion = "尝试其他"
            next_skill = self._get_next_skill(emotion_type)
            advice = f"这个技能有一定效果。我们可以尝试其他技能，比如「{next_skill}」。"
        else:
            next_suggestion = "建议休息"
            next_skill = ""
            advice = "这个技能可能不太适合现在的时机。休息一下也是可以的。"

        return {
            "response": NEXT_STEP_PROMPT.format(
                suggestion=next_suggestion, specific_advice=advice
            ),
            "response_type": "evaluation_result",
            "effectiveness": {
                "before_intensity": before_intensity,
                "after_intensity": after_intensity,
                "improvement": improvement,
                "result": effectiveness,
            },
            "should_end": False,
            "current_agent": self.AGENT_NAME,
            "next_action": "wait_summary",
            "next_suggestion": next_suggestion,
            "recommend_skill": next_skill,
        }

    def _get_next_skill(self, emotion_type: str) -> str:
        """获取下一个推荐技能"""
        skill_map = {
            "anxiety": ["正念呼吸", "接地技术", "一心一意"],
            "anger": ["STOP", "慢慢呼吸", "正念观察"],
            "sadness": ["自我安抚", "积极体验", "感恩练习"],
            "fear": ["安全空间想象", "渐进式放松", "正念呼吸"],
            "joy": ["正念享受", "感恩记录"],
            "calm": ["感恩练习", "价值澄清"],
        }
        return skill_map.get(emotion_type, ["正念呼吸"])[0]

    async def _generate_summary(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """生成对话总结"""
        emotion_type = state.get("current_emotion", {}).get("type", "未知")
        emotion_intensity = state.get("intensity", "未知")
        effectiveness = state.get("effectiveness")
        if isinstance(effectiveness, dict):
            effectiveness_result = effectiveness.get("result", "未知")
        else:
            effectiveness_result = "未知"
        skill_name = state.get("recommended_skill", {}).get("name", "未练习")

        summary = f"今天你因为{emotion_type}情绪（强度{emotion_intensity}分）来到这里，"
        summary += f"我们一起练习了「{skill_name}」。"
        summary += f"练习后你的情绪变化为：{effectiveness_result}。"

        return {
            "response": summary,
            "response_type": "summary",
            "session_summary": summary,
            "should_end": False,
            "current_agent": self.AGENT_NAME,
            "next_action": "wait_closing",
        }

    def _generate_closing(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """生成结束语"""
        summary = state.get("session_summary", "")
        closing = CLOSING_PROMPT.format(summary=summary)

        return {
            "response": closing,
            "response_type": "closing",
            "should_end": True,
            "current_agent": self.AGENT_NAME,
            "next_action": "session_end",
        }

    def _default_response(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """默认响应"""
        return {
            "response": "我理解你的感受。你还想继续练习其他技能，还是今天就到这里？",
            "response_type": "default",
            "should_end": False,
            "current_agent": self.AGENT_NAME,
            "next_action": "wait_user_choice",
        }
