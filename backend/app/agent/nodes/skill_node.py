"""
技能推荐节点
根据情绪状态推荐 DBT 技能（LLM 驱动）
"""

from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from langchain_core.messages import AIMessage
from app.agent.state import AgentState
from app.core.llm_client import get_llm_client
from app.dbt.skills import get_skill_info
from app.core.skill_recommender import SkillRecommender
from app.dbt.skills import SKILLS_DATABASE


def skill_recommendation_node(
    state: AgentState, db: Optional[Session] = None
) -> AgentState:
    """
    技能推荐节点

    1. 根据情绪状态调用 LLM 推荐技能
    2. 获取技能详情
    3. 生成推荐理由
    """
    if not state.get("current_emotion"):
        return state

    emotion = state["current_emotion"] or {}

    recommender = SkillRecommender(db)

    recommendation = recommender.recommend_skill(
        emotion_type=emotion.get("type") or "calm",
        intensity=emotion.get("intensity") or 5,
        user_id=state.get("user_id") or 0,
    )

    skill_name = recommendation.get("skill_name") or ""
    skill_info = SKILLS_DATABASE.get(skill_name, {})
    state["recommended_skill"] = {
        "name": skill_name,
        "category": skill_info.get("category", "mindfulness"),
        "reason": recommendation.get("reason", ""),
        "introduction": recommendation.get(
            "introduction", skill_info.get("introduction", "")
        ),
        "estimated_duration": recommendation.get("estimated_duration", "5-10分钟"),
    }
    state["skill_step"] = 0
    state["before_intensity"] = emotion.get("intensity") or 5

    messages = state.get("messages") or []
    last_msg_content = ""
    if messages:
        last_msg = messages[-1]
        content = last_msg.content
        last_msg_content = content if isinstance(content, str) else str(content)

    recommendation_message = _generate_recommendation_message(
        emotion=emotion,
        skill_name=skill_name,
        skill_info=skill_info,
        user_message=last_msg_content,
    )

    state["messages"] = list(state["messages"]) + [
        AIMessage(content=recommendation_message)
    ]

    state["next_action"] = "wait_skill_confirmation"

    return state


def _generate_recommendation_message(
    emotion: dict, skill_name: str, skill_info: dict, user_message: str = ""
) -> str:
    """
    生成技能推荐消息（使用LLM生成更自然的话术）

    Args:
        emotion: 情绪状态
        skill_name: 技能名称
        skill_info: 技能详细信息
        user_message: 用户原始消息

    Returns:
        推荐消息文本
    """
    llm_client = get_llm_client()

    # 情绪映射
    emotion_map = {
        "joy": "开心",
        "calm": "平静",
        "sadness": "悲伤",
        "anxiety": "焦虑",
        "anger": "愤怒",
        "fear": "恐惧",
    }

    emotion_type = emotion.get("type") if isinstance(emotion, dict) else "calm"
    emotion_cn = emotion_map.get(emotion_type or "", "这种感觉")
    intensity = emotion.get("intensity") or 5

    # 技能介绍
    introduction = skill_info.get("introduction", "")

    # 预计用时
    steps = skill_info.get("steps", [])
    estimated_time = f"{len(steps) * 2}-{len(steps) * 3}分钟"

    # 尝试使用LLM生成更个性化的推荐话术
    system_prompt = f"""你是一个温暖、专业的情绪支持助手。用户现在感到{emotion_cn}（强度{intensity}/10）。

你需要：
1. 先表达共情和理解（不要太长，1-2句话）
2. 推荐DBT技能「{skill_name}」
3. 简短介绍这个技能的作用：{introduction}
4. 告诉用户预计用时：{estimated_time}
5. 询问用户是否愿意尝试

要求：
- 语气温暖、鼓励，但不要过度热情
- 不要使用医学术语
- 使用1-2个合适的emoji
- 控制在150字以内
"""

    try:
        llm_response = llm_client.generate_response(
            system_prompt, user_message or f"我感到{emotion_cn}"
        )

        if llm_response:
            return llm_response

    except Exception as e:
        import logging

        logger = logging.getLogger(__name__)
        logger.warning(f"LLM生成推荐话术失败，使用模板: {str(e)}")

    # 回退到模板消息
    if intensity >= 7:
        empathy = f"我能感受到你现在很{emotion_cn}，这种感觉很强烈😔"
    elif intensity >= 5:
        empathy = f"听起来你现在有些{emotion_cn}，感觉不太好"
    else:
        empathy = f"注意到你有点{emotion_cn}的感觉"

    message = """{empathy}

你现在方便试试吗？如果方便，我会一步步带着你做💙""".format(empathy=empathy)

    return message
