"""
Agent状态定义
定义Agent在对话过程中维护的状态数据结构（LangGraph TypedDict）
"""

from typing import TypedDict, Annotated, Sequence, Dict, Optional, List
from langchain_core.messages import BaseMessage
import operator


class AgentState(TypedDict):
    """
    Agent 状态定义 (LangGraph TypedDict)

    使用 Annotated + operator.add 实现消息历史自动追加
    """

    # ========== 消息历史 ==========
    # 使用 operator.add 实现追加模式
    messages: Annotated[Sequence[BaseMessage], operator.add]

    # ========== 会话信息 ==========
    session_id: str
    user_id: int

    # ========== 情绪状态 ==========
    current_emotion: Optional[Dict]
    intensity: Optional[int]
    before_intensity: Optional[int]
    after_intensity: Optional[int]
    effectiveness: Optional[str]

    # ========== 身体感知 ==========
    body_sensation: Optional[Dict]

    # ========== 图片识别 ==========
    pending_image_urls: Optional[List[str]]
    image_recognition_attempts: int
    image_emotion: Optional[Dict]

    # ========== 识别AGENT输出 ==========
    identified_emotion: Optional[Dict]
    user_intention: Optional[str]
    needs_clarification: bool
    clarification_prompt: Optional[str]

    # ========== 危机检测 ==========
    is_crisis: bool
    risk_level: str
    crisis_trigger: Optional[str]
    emergency_detected: bool
    emergency_type: Optional[str]
    emergency_response: Optional[str]
    emergency_keywords: List[Dict]

    # ========== 技能系统 ==========
    recommended_skill: Optional[Dict]
    skill_step: int
    skill_history: List[Dict]
    skill_confidence: Optional[float]

    # ========== 干预引导AGENT输出 ==========
    guidance_state: Optional[Dict]

    # ========== 控制流 ==========
    current_agent: Optional[str]
    latest_message: Optional[str]
    should_end: bool
    requires_user_input: bool
    next_action: Optional[str]

    # ========== 会话总结 ==========
    session_summary: Optional[str]


def create_initial_state(session_id: str, user_id: int) -> AgentState:
    """
    创建初始状态

    Args:
        session_id: 会话ID
        user_id: 用户ID

    Returns:
        初始化的AgentState
    """
    return AgentState(
        session_id=session_id,
        user_id=user_id,
        messages=[],
        current_emotion=None,
        intensity=None,
        is_crisis=False,
        risk_level="low",
        crisis_trigger=None,
        recommended_skill=None,
        skill_step=-1,
        skill_history=[],
        before_intensity=None,
        after_intensity=None,
        effectiveness=None,
        body_sensation=None,
        pending_image_urls=None,
        image_recognition_attempts=0,
        image_emotion=None,
        should_end=False,
        requires_user_input=False,
        next_action=None,
        session_summary=None,
        identified_emotion=None,
        user_intention=None,
        emergency_detected=False,
        emergency_type=None,
        emergency_response=None,
        emergency_keywords=[],
        needs_clarification=False,
        clarification_prompt=None,
        skill_confidence=None,
        guidance_state=None,
        current_agent=None,
        latest_message=None,
    )
