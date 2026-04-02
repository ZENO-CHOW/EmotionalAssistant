"""
情绪识别节点
分析用户消息，识别情绪类型和强度（LLM 驱动）
"""

from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage, AIMessage
from app.agent.state import AgentState
from app.core.llm_client import get_llm_client
import logging

logger = logging.getLogger(__name__)


def emotion_recognition_node(
    state: AgentState, db: Optional[Session] = None
) -> AgentState:
    """
    情绪识别节点（增强版）

    优先级：
    1. image_emotion - 用户选择的情绪图片
    2. intensity - 用户选择的强度
    3. body_sensation - 用户选择的身体感知
    4. LLM 文本分析 - 原有逻辑
    """
    if not state["messages"]:
        return state

    latest_message = state["messages"][-1]
    if not isinstance(latest_message, HumanMessage):
        return state

    # 1. 优先使用用户选择的情绪图片
    image_emotion = state.get("image_emotion")
    if image_emotion:
        if state.get("intensity") is None:
            state["requires_user_input"] = True
            state["next_action"] = "wait_intensity_rating"
            logger.info("等待用户评估情绪强度")
            return state
        else:
            state["current_emotion"] = {
                "type": image_emotion.get("type"),
                "intensity": state.get("intensity"),
                "confidence": image_emotion.get("confidence", 0.9),
                "reason": image_emotion.get("reason", "用户选择的情绪图片"),
            }
            state["requires_user_input"] = False
            state["next_action"] = None
            logger.info(f"使用图片+强度: {state['current_emotion']}")
            return state

    # 2. 使用用户选择的强度
    if state.get("intensity") is not None:
        intensity = state["intensity"]
        current_emotion = state.get("current_emotion")
        if current_emotion:
            current_emotion["intensity"] = intensity
            state["requires_user_input"] = False
            state["next_action"] = None
            logger.info(f"更新情绪强度: {intensity}")
        else:
            state["requires_user_input"] = True
            state["next_action"] = "emotion_clarification"
            clarification_prompt = "我了解到你的情绪强度了。能再告诉我是什么情绪吗？比如开心、焦虑、难过..."
            state["messages"] = list(state["messages"]) + [
                AIMessage(content=clarification_prompt)
            ]
            logger.info(f"等待用户确认情绪类型，强度: {intensity}")
        return state

    # 3. 使用用户选择的身体感知辅助判断
    body_sensation = state.get("body_sensation")
    if body_sensation:
        selected_parts = (
            body_sensation.get("selected_parts", []) if body_sensation else []
        )
        part_names = body_sensation.get("part_names", {}) if body_sensation else {}
        logger.info(f"使用身体感知辅助: {part_names}")

    # 4. 调用 LLM 文本分析（原有逻辑）
    message_content = latest_message.content
    if isinstance(message_content, list):
        user_message = str(message_content)
    else:
        user_message = message_content

    history: list[dict[str, str]] = []
    for msg in state["messages"][-6:-1]:
        if isinstance(msg, HumanMessage):
            content = msg.content if isinstance(msg.content, str) else str(msg.content)
            history.append({"role": "user", "content": content})
        elif isinstance(msg, AIMessage):
            content = msg.content if isinstance(msg.content, str) else str(msg.content)
            history.append({"role": "assistant", "content": content})

    logger.info(f"传递 {len(history)} 条历史消息进行LLM情绪分析")

    llm = get_llm_client()
    text_message = user_message if isinstance(user_message, str) else str(user_message)
    emotion_result = llm.analyze_emotion(text_message, history) or {}

    if emotion_result.get("emotion_type"):
        state["current_emotion"] = {
            "type": emotion_result["emotion_type"],
            "intensity": emotion_result.get("intensity", 5),
            "confidence": emotion_result.get("confidence", 0.5),
            "reason": emotion_result.get("reason", ""),
        }

    if emotion_result.get("need_more_info"):
        state["requires_user_input"] = True
        state["next_action"] = "emotion_clarification"
        clarification_prompt = (
            _generate_clarification_prompt(emotion_result) if emotion_result else ""
        )
        state["messages"] = list(state["messages"]) + [
            AIMessage(content=clarification_prompt)
        ]
    else:
        state["requires_user_input"] = False
        state["next_action"] = None

    logger.info(f"LLM识别情绪结果: {state.get('current_emotion')}")
    return state


def _generate_clarification_prompt(emotion_result: Dict) -> str:
    """生成澄清提示"""
    emotion_type = emotion_result.get("emotion_type")

    if not emotion_type:
        return "我想更准确地理解你的感受。你现在的情绪是偏向开心、平静、难过、焦虑、生气，还是害怕呢？"

    emotion_map = {
        "joy": "开心",
        "calm": "平静",
        "sadness": "难过",
        "anxiety": "焦虑",
        "anger": "生气",
        "fear": "害怕",
    }

    emotion_cn = emotion_map.get(emotion_type, "这种感觉")
    return f"听起来你现在有些{emotion_cn}。能告诉我这种感觉有多强烈吗？从0（完全不明显）到10（非常强烈），你会给几分呢？"
