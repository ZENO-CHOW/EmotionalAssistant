"""
效果评估节点
评估技能练习效果（LLM + 规则双轨）
"""

from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from langchain_core.messages import AIMessage, HumanMessage
from app.agent.state import AgentState
from app.core.evaluator import Evaluator
from app.core.llm_client import get_llm_client


def effectiveness_evaluation_node(
    state: AgentState, db: Optional[Session] = None
) -> AgentState:
    """
    效果评估节点

    1. 记录训练前情绪强度
    2. 引导用户评估训练后感受
    3. 计算效果并记录
    """
    emotion = state.get("current_emotion") or {}
    before_intensity = emotion.get("intensity", 5) or 5

    if state.get("before_intensity") is None:
        state["before_intensity"] = before_intensity
        state["next_action"] = "request_evaluation"
        state["requires_user_input"] = True

        eval_prompt = """练习结束后，请评估你现在的情绪状态。

请给你的情绪强度打分（0-10）：
- 0：完全平静，没有任何负面情绪
- 5：中等程度
- 10：非常强烈

你现在感觉如何？强度几分？"""

        state["messages"] = list(state["messages"]) + [AIMessage(content=eval_prompt)]

        return state

    after_intensity = state.get("after_intensity")
    if after_intensity is None:
        for msg in reversed(state["messages"]):
            if isinstance(msg, HumanMessage):
                content = msg.content
                try:
                    text_content = content if isinstance(content, str) else str(content)
                    after_intensity = int(text_content.strip())
                    state["after_intensity"] = after_intensity
                except ValueError:
                    after_intensity = before_intensity
                    state["after_intensity"] = after_intensity
                break

    evaluator = Evaluator()
    recommended_skill = state.get("recommended_skill") or {}
    before_val = state.get("before_intensity") or before_intensity
    after_val = state.get("after_intensity") or before_intensity
    effectiveness = evaluator.evaluate_skill_effectiveness(
        before_intensity=before_val,
        after_intensity=after_val,
    )

    state["effectiveness"] = effectiveness

    llm = get_llm_client()
    feedback = _generate_feedback(state)

    state["messages"] = list(state["messages"]) + [AIMessage(content=feedback)]

    before_int = state.get("before_intensity") or 5
    after_int = state.get("after_intensity")
    improvement = before_int - after_int if after_int is not None else 0

    if improvement <= 0 and before_int >= 7:
        state["recommended_skill"] = None
        state["should_end"] = False
    else:
        state["should_end"] = True
        state["next_action"] = "generate_summary"

    return state


def _generate_feedback(state: AgentState) -> str:
    """生成效果反馈"""
    effectiveness = state.get("effectiveness") or "neutral"
    before_int = state.get("before_intensity") or 5
    after_int = state.get("after_intensity") or 5
    improvement = before_int - after_int
    recommended_skill = state.get("recommended_skill") or {}
    skill_name = recommended_skill.get("name") or ""

    feedback_map = {
        "effective": f"很高兴这个练习对你有帮助！通过{skill_name}，你成功降低了情绪强度。这说明你已经掌握了这项技能的核心要点。",
        "ineffective": f"看起来{skill_name}这次没有达到预期效果。这很正常，每个人的情况不同。重要的是你愿意尝试，我们可以换一种方法。",
        "neutral": f"这次练习后你的情绪有了一些变化。持续的练习会帮助你更好地掌握情绪调节的能力。",
    }

    return feedback_map.get(effectiveness, feedback_map["neutral"])
