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
    current_emotion: Optional[Dict]  # {
    #   "type": "anxiety",
    #   "intensity": 7,
    #   "confidence": 0.85,
    #   "reason": "用户表达了担忧和不安"
    # }
    intensity: Optional[int]  # 用户选择的情绪强度 (0-10)

    # ========== 危机检测 ==========
    is_crisis: bool
    risk_level: str  # low/medium/high/critical
    crisis_trigger: Optional[str]  # high_intensity/keywords/repeated_crisis

    # ========== 技能系统 ==========
    recommended_skill: Optional[Dict]  # {
    #   "name": "正念呼吸",
    #   "category": "mindfulness",
    #   "reason": "...",
    #   "introduction": "..."
    # }
    skill_step: int  # -1=未开始, 0=等待确认, >0=步骤进行中
    skill_history: List[Dict]  # [{"skill": "...", "effectiveness": "..."}]

    # ========== 效果评估 ==========
    before_intensity: Optional[int]
    after_intensity: Optional[int]
    effectiveness: Optional[str]  # effective/ineffective/neutral

    # ========== 身体感知 ==========
    body_sensation: Optional[Dict]  # {
    #   "selected_parts": ["head", "neck", "chest"],
    #   "part_names": {"head": "头部", "neck": "颈部", ...}
    # }

    # ========== 图片识别 ==========
    pending_image_urls: Optional[List[str]]  # 待识别的图片URL列表
    image_recognition_attempts: int  # 图片识别尝试次数
    image_emotion: Optional[Dict]  # {
    #   "type": "anxiety",
    #   "confidence": 0.85,
    #   "reason": "...",
    #   "source": "image_recognition"
    # }

    # ========== 识别AGENT输出 ==========
    identified_emotion: Optional[Dict]  # {
    #   "type": "anxiety",
    #   "intensity": 7,
    #   "confidence": 0.85,
    #   "reason": "..."
    # }
    user_intention: Optional[str]  # immediate_help/skill_learning/casual_talk
    emergency_detected: bool
    emergency_type: Optional[str]
    emergency_response: Optional[str]
    emergency_keywords: List[Dict]
    needs_clarification: bool
    clarification_prompt: Optional[str]

    # ========== 技能推荐AGENT输出 ==========
    skill_confidence: Optional[float]

    # ========== 干预引导AGENT输出 ==========
    guidance_state: Optional[Dict]  # {
    #   "current_step": 2,
    #   "total_steps": 4,
    #   "completed": False
    # }

    # ========== 控制流 ==========
    current_agent: Optional[str]  # recognition/recommendation/intervention
    latest_message: Optional[str]

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
