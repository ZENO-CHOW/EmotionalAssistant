"""
身体感知节点
引导用户描述情绪带来的身体感受
"""

import logging
from typing import Optional
from sqlalchemy.orm import Session
from langchain_core.messages import AIMessage
from app.agent.state import AgentState

logger = logging.getLogger(__name__)


def body_sensation_node(state: AgentState, db: Optional[Session] = None) -> AgentState:
    """
    身体感知节点

    在情绪识别后，引导用户关注身体感受

    Args:
        state: AgentState
        db: 数据库会话

    Returns:
        更新后的 AgentState
    """
    emotion = state.get("current_emotion")
    if not emotion:
        return state

    if state.get("body_sensation"):
        return state

    intensity = emotion.get("intensity", 5)
    if intensity < 4:
        return state

    body_prompt = _generate_body_prompt(emotion)

    state["next_action"] = "body_sensation"
    state["requires_user_input"] = True

    state["messages"] = list(state["messages"]) + [AIMessage(content=body_prompt)]

    logger.info(f"触发身体感知引导，强度: {intensity}")

    return state


def _generate_body_prompt(emotion: dict) -> str:
    """生成身体感知引导话术"""
    emotion_map = {
        "anxiety": "焦虑",
        "sadness": "难过",
        "anger": "愤怒",
        "fear": "害怕",
        "joy": "开心",
        "calm": "平静",
    }

    emotion_type = emotion.get("type") if emotion else None
    emotion_cn = (
        emotion_map.get(emotion_type, "这种感受") if emotion_type else "这种感受"
    )
    intensity = emotion.get("intensity", 5)

    if intensity >= 7:
        prompt = f"""谢谢你告诉我你感到{emotion_cn}，我能感受到你现在很不舒服。

情绪和身体往往是相连的——你现在身体有哪里不舒服的感觉吗？比如：
- 胸口：闷、紧、痛
- 头部：胀、晕、痛
- 胃部：不舒服、恶心
- 其他部位

可以选择一个部位，我会帮你针对性地缓解。"""
    elif intensity >= 4:
        prompt = f"""了解到你有些{emotion_cn}。

有时候情绪会在身体上有所体现。你现在身体有哪里不舒服的感觉吗？可以简单描述一下。"""
    else:
        prompt = f"""好的，了解到你感到{emotion_cn}。

一般这个时候身体感觉怎么样？有什么想说的吗？"""

    return prompt
