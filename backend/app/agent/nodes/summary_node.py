"""
会话总结节点
生成会话总结（LLM 驱动）
"""

from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from langchain_core.messages import AIMessage, HumanMessage
from app.agent.state import AgentState
from app.core.llm_client import get_llm_client


def session_summary_node(state: AgentState, db: Optional[Session] = None) -> AgentState:
    """
    会话总结节点

    1. 生成对话总结
    2. 生成关闭语
    """
    messages = []
    for msg in state["messages"]:
        if hasattr(msg, "role"):
            messages.append({"role": msg.role, "content": msg.content})
        else:
            messages.append({"role": "unknown", "content": str(msg)})

    llm = get_llm_client()

    summary_prompt = f"""请对以下对话进行总结，生成一份简洁的会话报告：

对话内容：
{chr(10).join([f"{m['role']}: {m['content'][:100]}..." if len(m["content"]) > 100 else f"{m['role']}: {m['content']}" for m in messages])}

情绪变化：{state.get("before_intensity", "?")} → {state.get("after_intensity", "?")}
使用的技能：{state.get("recommended_skill", {}).get("name", "无")}

请以 JSON 格式返回：
{{
  "summary": "2-3句话的对话摘要",
  "emotions_experienced": ["经历的主要情绪"],
  "skills_practiced": ["练习的技能"],
  "overall_assessment": "整体评估（积极/中性/需关注）"
}}"""

    try:
        summary_result = llm.analyze_emotion(summary_prompt, messages[-5:])
        summary = summary_result.get("summary", "这是一次情绪管理对话。")
    except Exception:
        summary = "这是一次情绪管理对话，你分享了自己的感受并尝试了调节技能。"

    state["session_summary"] = summary

    closing_prompt = """请生成一段温暖的结束语，对用户今天的练习给予肯定和鼓励。

要求：
1. 感谢用户的参与和努力
2. 肯定用户的进步（如果有）
3. 鼓励用户在日常生活中继续练习
4. 提醒可以随时回来寻求帮助
5. 语言温暖、简洁（50字以内）"""

    closing = llm.generate_response(
        system_prompt=closing_prompt, user_message="生成关闭语"
    )

    state["messages"] = list(state["messages"]) + [AIMessage(content=closing)]
    state["should_end"] = True

    return state
