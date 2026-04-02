"""
LangGraph 状态图构建器
使用 LangGraph 官方 API 构建 Agent 状态图
"""

from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from app.agent.state import AgentState
from app.agent.nodes import (
    emotion_recognition_node,
    crisis_detection_node,
    crisis_intervention_node,
    skill_recommendation_node,
    skill_guidance_node,
    effectiveness_evaluation_node,
    session_summary_node,
    image_recognition_node,
    body_sensation_node,
    intensity_assessment_node,
)


def create_agent_graph(checkpointer=None):
    """
    创建 Agent 状态图

    Args:
        checkpointer: 状态持久化器（可选）

    Returns:
        编译后的 StateGraph
    """
    workflow = StateGraph(AgentState)

    workflow.add_node("image_recognition", image_recognition_node)
    workflow.add_node("intensity_assessment", intensity_assessment_node)
    workflow.add_node("emotion_recognition", emotion_recognition_node)
    workflow.add_node("body_sensation", body_sensation_node)
    workflow.add_node("crisis_detection", crisis_detection_node)
    workflow.add_node("crisis_intervention", crisis_intervention_node)
    workflow.add_node("skill_recommendation", skill_recommendation_node)
    workflow.add_node("skill_guidance", skill_guidance_node)
    workflow.add_node("effectiveness_evaluation", effectiveness_evaluation_node)
    workflow.add_node("summary_generation", session_summary_node)

    workflow.set_entry_point("emotion_recognition")

    workflow.add_conditional_edges(
        "image_recognition",
        _route_after_image_recognition,
        {
            "emotion_recognition": "emotion_recognition",
            "intensity_assessment": "intensity_assessment",
        },
    )

    workflow.add_conditional_edges(
        "intensity_assessment",
        _route_after_intensity_assessment,
        {
            "emotion_recognition": "emotion_recognition",
        },
    )

    workflow.add_edge("crisis_intervention", END)
    workflow.add_edge("summary_generation", END)

    workflow.add_conditional_edges(
        "emotion_recognition",
        _route_after_emotion_recognition,
        {
            "image_recognition": "image_recognition",
            "body_sensation": "body_sensation",
            "crisis_detection": "crisis_detection",
        },
    )

    workflow.add_conditional_edges(
        "body_sensation",
        _route_after_body_sensation,
        {
            "crisis_detection": "crisis_detection",
        },
    )

    workflow.add_conditional_edges(
        "crisis_detection",
        _route_after_crisis_detection,
        {
            "crisis_intervention": "crisis_intervention",
            "skill_recommendation": "skill_recommendation",
        },
    )

    workflow.add_conditional_edges(
        "skill_recommendation",
        _route_after_recommendation,
        {
            "skill_guidance": "skill_guidance",
            "effectiveness_evaluation": "effectiveness_evaluation",
        },
    )

    workflow.add_conditional_edges(
        "skill_guidance",
        _route_after_guidance,
        {
            "continue_guidance": "skill_guidance",
            "effectiveness_evaluation": "effectiveness_evaluation",
            "end": END,
        },
    )

    workflow.add_conditional_edges(
        "effectiveness_evaluation",
        _route_after_evaluation,
        {
            "summary_generation": "summary_generation",
            "skill_recommendation": "skill_recommendation",
            "end": END,
        },
    )

    return workflow.compile(checkpointer=checkpointer)


def _route_after_image_recognition(state: AgentState) -> str:
    """图片识别后的路由逻辑"""
    if state.get("pending_image_urls"):
        return "image_recognition"

    if state.get("image_emotion") and state.get("intensity") is None:
        return "intensity_assessment"

    return "emotion_recognition"


def _route_after_intensity_assessment(state: AgentState) -> str:
    """强度评估后的路由逻辑"""
    if state.get("intensity") is not None:
        return "emotion_recognition"
    return "emotion_recognition"


def _route_after_emotion_recognition(state: AgentState) -> str:
    """情绪识别后的路由逻辑"""
    if state.get("pending_image_urls"):
        return "image_recognition"
    if (
        state.get("requires_user_input")
        and state.get("next_action") == "body_sensation"
    ):
        return "body_sensation"
    return "crisis_detection"


def _route_after_body_sensation(state: AgentState) -> str:
    """身体感知后的路由逻辑"""
    if state.get("body_sensation"):
        return "crisis_detection"
    return "crisis_detection"


def _route_after_crisis_detection(state: AgentState) -> str:
    """危机检测后的路由逻辑"""
    if state.get("is_crisis"):
        return "crisis_intervention"
    return "skill_recommendation"


def _route_after_recommendation(state: AgentState) -> str:
    """技能推荐后的路由逻辑"""
    if state.get("recommended_skill"):
        skill_step = state.get("skill_step", -1)
        if skill_step == -1 or skill_step == 0:
            return "skill_guidance"
    return "effectiveness_evaluation"


def _route_after_guidance(state: AgentState) -> str:
    """技能引导后的路由逻辑"""
    skill_step = state.get("skill_step", -1)

    if skill_step > 0 and skill_step != -1:
        return "continue_guidance"
    elif skill_step == -1:
        return "effectiveness_evaluation"
    else:
        return "end"


def _route_after_evaluation(state: AgentState) -> str:
    """效果评估后的路由逻辑"""
    if state.get("should_end"):
        return "summary_generation"
    if state.get("recommended_skill") is None:
        return "skill_recommendation"
    return "end"


def create_agent_with_memory():
    """创建带内存持久化的 Agent（开发环境）"""
    checkpointer = MemorySaver()
    return create_agent_graph(checkpointer=checkpointer)

