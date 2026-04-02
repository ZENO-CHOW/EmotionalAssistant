"""
强度评估节点
处理用户选择情绪图片后的强度评估流程
"""

from typing import Dict, Any, Optional
from langchain_core.messages import AIMessage
from app.agent.state import AgentState
import logging

logger = logging.getLogger(__name__)


def intensity_assessment_node(
    state: AgentState,
) -> AgentState:
    """
    强度评估节点

    用户选择情绪图片后，触发强度评估
    """
    if state.get("image_emotion") and state.get("intensity") is None:
        state["requires_user_input"] = True
        state["next_action"] = "wait_intensity_rating"
        logger.info("触发强度评估流程")
        return state

    if state.get("intensity") is not None:
        state["requires_user_input"] = False
        state["next_action"] = None
        return state

    return state
