"""
技能引导节点
引导用户练习 DBT 技能（LLM 动态生成话术）
"""

from typing import Dict, Optional
from sqlalchemy.orm import Session
from langchain_core.messages import AIMessage, HumanMessage
from app.agent.state import AgentState
from app.core.llm_client import get_llm_client
from app.dbt.skills import get_skill_info, get_skill_steps


def skill_guidance_node(state: AgentState, db: Optional[Session] = None) -> AgentState:
    """
    技能引导节点

    1. 根据当前步骤生成引导话术
    2. 逐步引导用户完成技能练习
    """
    skill = state.get("recommended_skill")
    if not skill:
        return state

    skill_name = skill.get("name") or ""
    skill_step = state.get("skill_step", -1)

    if not skill_name:
        return state

    skill_info = get_skill_info(skill_name) or {}
    steps = get_skill_steps(skill_name) or []

    if skill_step == 0:
        return _handle_skill_confirmation(state, skill_info, steps)

    if skill_step > 0 and skill_step <= len(steps):
        if state.get("step_completed"):
            next_step = skill_step + 1
            state["step_completed"] = False
            if next_step > len(steps):
                state["skill_step"] = -1
                state["requires_user_input"] = False
                state["next_action"] = "skill_completed"
                state["guidance_state"] = {
                    "current_step": len(steps),
                    "total_steps": len(steps),
                    "completed": True,
                    "waiting_for_input": False,
                }
                return state

            state["skill_step"] = next_step
            return _handle_skill_step(state, skill_info, steps, next_step)

        return _handle_skill_step(state, skill_info, steps, skill_step)

    return state


def _handle_skill_confirmation(
    state: AgentState, skill_info: Dict, steps: list
) -> AgentState:
    """处理技能开始前的确认"""
    confirmation = state.get("skill_confirmation") or {}
    accepted = confirmation.get("accepted")

    if accepted is True:
        state["skill_confirmation"] = None
        if not steps:
            state["skill_step"] = -1
            state["requires_user_input"] = False
            state["next_action"] = "skill_completed"
            state["guidance_state"] = {
                "current_step": 0,
                "total_steps": 0,
                "completed": True,
                "waiting_for_input": False,
            }
            return state

        state["skill_step"] = 1
        state["requires_user_input"] = False
        state["next_action"] = None
        return _handle_skill_step(state, skill_info, steps, 1)

    if accepted is False:
        skill_name = skill_info.get("name", "这个练习")
        response = f"没关系，我们不急着开始「{skill_name}」。你可以继续跟我说说现在的感受，或者等准备好了再试。"
        state["messages"] = list(state["messages"]) + [AIMessage(content=response)]
        state["skill_confirmation"] = None
        state["requires_user_input"] = False
        state["next_action"] = None
        state["should_end"] = False
        return state

    skill_name = skill_info.get("name", "")
    introduction = skill_info.get("introduction", "")

    confirmation_prompt = f"""请你邀请用户练习「{skill_name}」。

技能简介：{introduction}
预计用时：{skill_info.get("estimated_duration", "5-10分钟")}

要求：
1. 简短说明这个练习做什么
2. 告知需要的条件（如安静环境）
3. 询问用户是否方便现在练习
4. 语言温暖、不强迫

直接生成邀请语，不需要JSON格式。"""

    llm = get_llm_client()
    if getattr(llm, "client", None):
        response = llm.generate_response(
            system_prompt=confirmation_prompt, user_message="生成邀请语"
        )
    else:
        response = (
            f"我想邀请你试试「{skill_name}」。{introduction}"
            "这个练习大约需要5-10分钟，找一个相对安静、不被打扰的地方就可以。"
            "你现在方便开始吗？"
        )

    state["messages"] = list(state["messages"]) + [AIMessage(content=response)]
    state["requires_user_input"] = True
    state["next_action"] = "wait_skill_confirmation"
    state["guidance_state"] = {
        "current_step": 0,
        "total_steps": len(steps),
        "completed": False,
        "waiting_for_input": True,
    }

    return state


def _handle_skill_step(
    state: AgentState, skill_info: Dict, steps: list, step_num: int
) -> AgentState:
    """处理技能步骤引导"""
    skill_name = skill_info.get("name", "")
    step_content = steps[step_num - 1] if step_num <= len(steps) else ""

    user_context = ""
    for msg in state["messages"][-3:]:
        if isinstance(msg, HumanMessage):
            content = msg.content
            user_context = content if isinstance(content, str) else str(content)
            break

    llm = get_llm_client()
    if getattr(llm, "client", None):
        guidance = llm.generate_guidance(
            skill_name=skill_name,
            skill_category=skill_info.get("category", ""),
            total_steps=len(steps),
            current_step=step_num,
            step_content=step_content,
            user_context=user_context,
        )
    else:
        guidance = _format_step_message(skill_name, step_num, len(steps), step_content)

    state["messages"] = list(state["messages"]) + [AIMessage(content=guidance)]

    if step_num < len(steps):
        state["next_action"] = "wait_step_completion"
        state["requires_user_input"] = True
        state["guidance_state"] = {
            "current_step": step_num,
            "total_steps": len(steps),
            "content": step_content,
            "completed": False,
            "waiting_for_input": True,
            "is_last_step": False,
        }
    else:
        state["next_action"] = "wait_step_completion"
        state["requires_user_input"] = True
        state["guidance_state"] = {
            "current_step": step_num,
            "total_steps": len(steps),
            "content": step_content,
            "completed": False,
            "waiting_for_input": True,
            "is_last_step": True,
        }

    return state


def _format_step_message(
    skill_name: str, step_num: int, total_steps: int, step_content: str
) -> str:
    """LLM不可用时的步骤引导模板。"""
    opening = f"很好，我们开始练习「{skill_name}」。\n\n" if step_num == 1 else ""
    return (
        f"{opening}步骤 {step_num}/{total_steps}\n\n"
        f"{step_content}\n\n"
        "完成后告诉我，我会继续带你进行下一步。"
    )


def _generate_guidance_message(
    skill_name: str,
    step_number: int,
    total_steps: int,
    step_info: dict,
    is_first_step: bool,
    is_last_step: bool,
) -> str:
    """
    生成引导话术（使用LLM生成更自然的引导）

    Args:
        skill_name: 技能名称
        step_number: 当前步骤编号
        total_steps: 总步骤数
        step_info: 步骤信息
        is_first_step: 是否第一步
        is_last_step: 是否最后一步

    Returns:
        引导话术文本
    """
    llm_client = get_llm_client()

    step_title = step_info.get("title", "")
    step_description = step_info.get("description", "")
    step_duration = step_info.get("duration", "")
    step_guidance = step_info.get("guidance", "")

    # 尝试使用LLM生成更个性化的引导话术
    system_prompt = f"""你是一个温柔、耐心的DBT技能引导师。你正在带领用户完成「{skill_name}」练习。

当前是第{step_number}/{total_steps}步：{step_title}
步骤说明：{step_description}
{f"具体指导：{step_guidance}" if step_guidance else ""}
{f"预计时间：{step_duration}" if step_duration else ""}

请生成一段引导话术，要求：
1. {'先说"很好，我们开始吧😊"' if is_first_step else ""}
2. 清楚地说明这一步要做什么
3. 语气温柔、鼓励
4. {'结尾说"完成后告诉我你现在的感觉吧💙"' if is_last_step else '结尾说"完成后回复我，我会告诉你下一步～"'}
5. 控制在100字以内
"""

    try:
        messages = [{"role": "user", "content": f"请引导我完成第{step_number}步"}]
        llm_response = llm_client.chat(
            messages, system_prompt=system_prompt, temperature=0.7, max_tokens=200
        )

        if llm_response:
            return llm_response

    except Exception as e:
        import logging

        logger = logging.getLogger(__name__)
        logger.warning(f"LLM生成引导话术失败，使用模板: {str(e)}")

    # 回退到模板消息
    # 开头
    if is_first_step:
        opening = f"很好，我们开始吧😊\n\n"
    else:
        opening = ""

    # 步骤说明
    step_indicator = f"第{step_number}步/{total_steps}步：{step_title}"

    if step_duration:
        step_indicator += f"（{step_duration}）"

    # 具体指令
    instruction = f"\n{step_description}"

    # 结尾
    if is_last_step:
        closing = "\n\n完成后告诉我你现在的感觉吧💙"
    else:
        closing = "\n\n完成后回复我，我会告诉你下一步～"

    return opening + step_indicator + instruction + closing
