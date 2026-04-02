"""
技能引导逻辑
处理多步骤技能练习的引导流程
"""

from typing import Dict, List, Any, Optional
from enum import Enum


class GuidanceState(Enum):
    """引导状态"""

    WAITING_CONFIRMATION = "waiting_confirmation"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"
    DECLINED = "declined"


class SkillGuidance:
    """技能引导器"""

    def __init__(self):
        self.state = GuidanceState.WAITING_CONFIRMATION
        self.current_step = 0
        self.total_steps = 0
        self.skill_data = None
        self.user_responses = []

    def initialize_guidance(self, skill_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        初始化技能引导

        Args:
            skill_data: 技能数据字典

        Returns:
            引导初始化结果
        """
        self.skill_data = skill_data
        self.state = GuidanceState.WAITING_CONFIRMATION
        self.current_step = 0
        self.user_responses = []

        steps = skill_data.get("steps", [])
        self.total_steps = len(steps) if steps else 0

        return {
            "state": self.state.value,
            "skill_name": skill_data.get("name", ""),
            "skill_introduction": skill_data.get("introduction", ""),
            "total_steps": self.total_steps,
            "current_step": self.current_step,
            "waiting_for_input": True,
        }

    def handle_confirmation(self, confirmed: bool) -> Dict[str, Any]:
        """
        处理用户确认

        Args:
            confirmed: 用户是否确认开始练习

        Returns:
            引导响应
        """
        if not self.skill_data:
            return {"error": "Guidance not initialized"}

        if confirmed:
            self.state = GuidanceState.IN_PROGRESS
            self.current_step = 1
            return self._get_current_step_response()
        else:
            self.state = GuidanceState.DECLINED
            return {
                "state": self.state.value,
                "response": "没关系。如果你改变主意，随时可以尝试。",
                "waiting_for_input": False,
                "should_end": True,
            }

    def handle_step_response(self, user_response: str) -> Dict[str, Any]:
        """
        处理用户对当前步骤的响应

        Args:
            user_response: 用户的响应

        Returns:
            引导响应
        """
        if not self.skill_data:
            return {"error": "Guidance not initialized"}

        if self.state != GuidanceState.IN_PROGRESS:
            return {"error": "Guidance not in progress"}

        self.user_responses.append(
            {"step": self.current_step, "response": user_response}
        )

        if self.current_step < self.total_steps:
            self.current_step += 1
            return self._get_current_step_response()
        else:
            self.state = GuidanceState.COMPLETED
            return {
                "state": self.state.value,
                "response": "太好了！你已经完成了这个技能的所有步骤。",
                "waiting_for_input": True,
                "completed": True,
            }

    def _get_current_step_response(self) -> Dict[str, Any]:
        """获取当前步骤的引导响应"""
        if not self.skill_data:
            return {"error": "Guidance not initialized"}
        steps = self.skill_data.get("steps", [])
        current_step_data = steps[self.current_step - 1] if steps else {}

        return {
            "state": self.state.value,
            "skill_name": self.skill_data.get("name", ""),
            "current_step": self.current_step,
            "total_steps": self.total_steps,
            "step_title": current_step_data.get("title", ""),
            "step_description": current_step_data.get("description", ""),
            "step_guidance": current_step_data.get("guidance", ""),
            "waiting_for_input": True,
            "completed": False,
        }

    def get_guidance_status(self) -> Dict[str, Any]:
        """
        获取当前引导状态

        Returns:
            状态字典
        """
        return {
            "state": self.state.value,
            "skill_name": self.skill_data.get("name") if self.skill_data else None,
            "current_step": self.current_step,
            "total_steps": self.total_steps,
            "completed_steps": len(self.user_responses),
            "waiting_for_input": self.state == GuidanceState.IN_PROGRESS,
        }

    def should_evaluate_effectiveness(self) -> bool:
        """检查是否需要进行效果评估"""
        return self.state == GuidanceState.COMPLETED

    def should_end_session(self) -> bool:
        """检查是否应该结束会话"""
        return self.state in [GuidanceState.COMPLETED, GuidanceState.DECLINED]


def format_guidance_message(step_data: Dict[str, Any], skill_name: str) -> str:
    """
    格式化技能引导消息

    Args:
        step_data: 步骤数据
        skill_name: 技能名称

    Returns:
        格式化的引导消息
    """
    message = f"现在我们来练习「{skill_name}」。\n\n"
    message += f"{step_data.get('description', '')}\n\n"
    message += f"**步骤 {step_data.get('step', '?')}/{step_data.get('total_steps', '?')}**：{step_data.get('title', '')}\n\n"
    message += f"请按以下指导进行：\n{step_data.get('guidance', '')}\n\n"
    message += "准备好了吗？完成后告诉我你的感受。"

    return message


def generate_skill_confirmation_message(skill_data: Dict[str, Any]) -> str:
    """
    生成技能确认消息

    Args:
        skill_data: 技能数据

    Returns:
        确认消息
    """
    name = skill_data.get("name", "")
    introduction = skill_data.get("introduction", "")
    steps_count = len(skill_data.get("steps", []))

    message = f"我推荐你尝试「{name}」。\n\n"
    message += f"{introduction}\n\n"
    message += f"这个技能包含 {steps_count} 个步骤，练习时间约 5-10 分钟。\n\n"
    message += "你愿意尝试这个技能吗？"

    return message


def get_alternative_skills(skill_name: str, emotion_type: str) -> List[str]:
    """
    获取替代技能列表

    Args:
        skill_name: 当前技能名称
        emotion_type: 情绪类型

    Returns:
        替代技能名称列表
    """
    alternative_map = {
        "TIPP": ["接地技术", "正念呼吸", "STOP"],
        "正念呼吸": ["一心一意", "节律呼吸", "观察、描述、参与"],
        "接地技术": ["安全空间想象", "正念观察", "5-4-3-2-1技术"],
        "情绪命名": ["观察、描述、参与", "无评判态度", "正念观察"],
        "自我安抚": ["安全空间想象", "渐进式放松", "正念享受"],
        "驾驭情绪之波": ["激进接纳", "观察、描述、参与", "利弊分析"],
    }

    alternatives = alternative_map.get(skill_name, [])
    return [alt for alt in alternatives if alt != skill_name]
