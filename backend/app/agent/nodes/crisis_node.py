"""
危机检测节点
检测用户是否处于危机状态（关键词 + LLM 双轨检测）
"""

from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from langchain_core.messages import AIMessage, HumanMessage
from app.agent.state import AgentState
from app.core.crisis_detector import CrisisDetector
from app.core.llm_client import get_llm_client


def crisis_detection_node(
    state: AgentState, db: Optional[Session] = None
) -> AgentState:
    """
    危机检测节点

    1. 规则引擎快速检测（关键词 + 阈值）
    2. LLM 二次确认（语义分析）
    3. 更新危机状态
    """
    if not state.get("current_emotion"):
        return state

    detector = CrisisDetector(db_session=db)
    emotion = state.get("current_emotion") or {}

    user_message = ""
    for msg in reversed(state["messages"]):
        if isinstance(msg, HumanMessage):
            content = msg.content
            user_message = content if isinstance(content, str) else str(content)
            break

    crisis_result = detector.detect_crisis(
        user_id=state.get("user_id", 0),
        message=user_message,
        intensity=emotion.get("intensity", 5),
        session_id=state.get("session_id", ""),
    )

    if crisis_result.get("is_crisis") or emotion.get("intensity", 0) >= 7:
        llm_confirm = _llm_crisis_confirm(user_message, emotion) or {}
        if llm_confirm.get("is_crisis"):
            crisis_result["is_crisis"] = True
            crisis_result["risk_level"] = llm_confirm.get(
                "risk_level", crisis_result.get("level", "medium")
            )

    state["is_crisis"] = crisis_result.get("is_crisis", False)
    state["risk_level"] = crisis_result.get("risk_level", "low")
    state["crisis_trigger"] = crisis_result.get("trigger_type")

    return state


def crisis_intervention_node(
    state: AgentState, db: Optional[Session] = None
) -> AgentState:
    """
    危机干预节点

    生成共情干预话术，提供危机资源
    """
    risk_level = state.get("risk_level", "medium")

    llm = get_llm_client()

    user_context = {
        "emotion": state.get("current_emotion", {}),
        "risk_level": risk_level,
    }

    intervention_prompt = f"""你是一位专业的心理咨询师，用户正经历情绪危机（风险等级：{risk_level}）。

请生成干预话术，要求：
1. 先表达共情和理解
2. 提供具体的危机应对建议
3. 告知专业求助资源
4. 语言温暖但不煽情
5. 长度控制在150字以内

当前用户情绪状态：{user_context}"""

    response = llm.generate_response(
        system_prompt=intervention_prompt,
        user_message="请帮助我生成危机干预话术",
        context=user_context,
    )

    state["messages"] = list(state["messages"]) + [AIMessage(content=response)]

    state["requires_user_input"] = False
    state["should_end"] = True
    state["next_action"] = "crisis_intervention_complete"

    return state


def _llm_crisis_confirm(user_message: str, emotion: Dict) -> Dict:
    """LLM 危机确认（语义分析）"""
    llm = get_llm_client()

    prompt = f"""请分析以下用户消息是否表达自杀/自残/绝望等危机信号：

用户消息：{user_message}
情绪强度：{emotion.get("intensity", 5)}/10

请以 JSON 格式返回分析结果：
{{
  "is_crisis": true/false,
  "risk_level": "low/medium/high/critical",
  "reason": "判断依据"
}}

注意：
- 如果用户表达不想活、绝望、无价值感等，视为危机
- 如果只是普通情绪困扰，不视为危机
- 宁可误报也不要漏报"""

    try:
        result = llm.analyze_emotion(prompt, []) or {}
        return result
    except Exception:
        return {"is_crisis": False, "risk_level": "low"}
