"""
对话API路由（LangGraph + LLM 升级版）
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, AsyncGenerator, Dict
import json
import logging
import re

from app.database.connection import get_db
from app.database.repositories.chat_repo import ChatRepository
from app.models.chat import (
    ChatMessageRequest,
    ChatMessageResponse,
    ChatHistoryResponse,
    SessionListResponse,
    SessionListItem,
    MessageItem,
    EmotionChange,
    RequiresInputSchema,
    MessageType,
)
from app.agent.state import create_initial_state
from app.agent.coordinator import coordinator
from app.agent.langgraph_builder import create_agent_graph, create_agent_with_memory
from app.core.dependencies import get_current_user_id
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

logger = logging.getLogger(__name__)
router = APIRouter()

_checkpointer = MemorySaver()

BODY_PART_NAMES = {
    "head": "头部",
    "neck": "颈部",
    "left_shoulder": "左肩",
    "right_shoulder": "右肩",
    "chest": "胸部",
    "left_arm": "左上臂",
    "right_arm": "右上臂",
    "left_forearm": "左前臂",
    "right_forearm": "右前臂",
    "left_hand": "左手",
    "right_hand": "右手",
    "abdomen": "腹部",
    "pelvis": "骨盆",
    "left_thigh": "左大腿",
    "right_thigh": "右大腿",
    "left_calf": "左小腿",
    "right_calf": "右小腿",
    "left_foot": "左脚",
    "right_foot": "右脚",
}


def parse_body_selection(metadata: Optional[Dict]) -> Optional[Dict]:
    """解析身体部位选择数据

    Args:
        metadata: 前端发送的元数据，应包含 selected_parts 数组

    Returns:
        解析后的身体感知数据，或 None
    """
    if not metadata:
        return None

    selected_parts = metadata.get("selected_parts")
    if not selected_parts or not isinstance(selected_parts, list):
        return None

    part_names = {part: BODY_PART_NAMES.get(part, part) for part in selected_parts}

    return {
        "selected_parts": selected_parts,
        "part_names": part_names,
        "part_count": len(selected_parts),
    }


def parse_user_input(request: ChatMessageRequest) -> dict:
    """解析用户输入类型，更新状态字段

    Args:
        request: ChatMessageRequest 请求对象

    Returns:
        包含 parsed_intensity, parsed_body_sensation, parsed_image_emotion, parsed_pending_image_url 的字典
    """
    parsed = {
        "intensity": None,
        "body_sensation": None,
        "image_emotion": None,
        "pending_image_urls": None,
    }

    if request.message_type == MessageType.INTENSITY_RATING:
        parsed["intensity"] = request.metadata.get("value")
        logger.info(f"解析强度选择: {parsed['intensity']}")

    elif request.message_type == MessageType.BODY_SELECTION:
        parsed["body_sensation"] = parse_body_selection(request.metadata)
        if parsed["body_sensation"]:
            logger.info(f"解析身体部位选择: {parsed['body_sensation']}")

    elif request.message_type == MessageType.IMAGE_SELECTION:
        parsed["image_emotion"] = request.metadata.get("emotion_type")
        image_urls = request.metadata.get("image_urls")
        parsed["pending_image_urls"] = image_urls if image_urls else []
        logger.info(
            f"解析图片选择: image_emotion={parsed['image_emotion']}, pending_image_urls={len(parsed['pending_image_urls'])}张图片"
        )

    return parsed


def clean_llm_response(text: str) -> str:
    """
    清理LLM响应中的不需要的格式
    - 移除括号中的语气描述，如（轻声）、（微笑）、（温柔地）等
    """
    if not text:
        return text

    # 移除中文括号中的语气描述
    text = re.sub(r"[（(][^）)]*[）)]", "", text)

    # 清理多余的空格
    text = re.sub(r"\s+", " ", text).strip()

    return text


def get_assessment_data(session) -> dict:
    """获取会话的评估数据"""
    if session.assessment_data:
        return json.loads(session.assessment_data)
    return {"message_count": 0, "step": "not_started"}


def update_assessment_data(repo: ChatRepository, session_id: str, data: dict):
    """更新会话的评估数据"""
    repo.update_session(
        session_id, {"assessment_data": json.dumps(data, ensure_ascii=False)}
    )


@router.post("/chat/message", response_model=ChatMessageResponse)
async def send_message(
    request: ChatMessageRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """
    发送对话消息（LangGraph 驱动）

    支持流式输出和非流式输出两种模式
    """
    try:
        repo = ChatRepository(db)

        if request.session_id:
            session = repo.get_session(request.session_id)
            if not session:
                raise HTTPException(
                    status_code=404, detail={"code": 404, "message": "会话不存在"}
                )
        else:
            session = repo.create_session(user_id)

        history_messages = repo.get_messages(session.id, limit=20)
        history_messages.reverse()

        messages = []
        for msg in history_messages:
            if msg.role == "user":
                messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                messages.append(AIMessage(content=msg.content))

        messages.append(HumanMessage(content=request.message))

        repo.save_message(
            session_id=session.id,
            role="user",
            content=request.message,
            message_type=request.message_type.value
            if hasattr(request.message_type, "value")
            else "text",
            metadata=request.metadata,
        )

        # 获取评估数据并检查是否需要触发评估
        assessment_data = get_assessment_data(session)
        logger.info(
            f"Assessment data before: {assessment_data}, message_type: {request.message_type.value}"
        )

        # 如果是文本消息，增加消息计数
        if request.message_type.value == "text":
            assessment_data["message_count"] = (
                assessment_data.get("message_count", 0) + 1
            )
            update_assessment_data(repo, session.id, assessment_data)
            logger.info(
                f"Assessment data after update: {assessment_data}, assessment_status: {session.assessment_status}"
            )

            # 检查是否需要触发评估（5条消息后且未开始评估）
            if (
                assessment_data["message_count"] >= 5
                and session.assessment_status == "not_started"
            ):
                logger.info(
                    f"🎯 TRIGGERING ASSESSMENT! message_count={assessment_data['message_count']}, status={session.assessment_status}"
                )
                # 触发评估流程
                repo.update_session(session.id, {"assessment_status": "in_progress"})
                assessment_data["step"] = "awaiting_image"
                update_assessment_data(repo, session.id, assessment_data)

                # 生成引导消息
                from app.core.llm_client import get_llm_client

                llm_client = get_llm_client()

                # 构建消息历史
                history_for_prompt = []
                for msg in history_messages:
                    history_for_prompt.append(
                        {"role": msg.role, "content": msg.content}
                    )
                history_for_prompt.append({"role": "user", "content": request.message})

                system_prompt = """你是小安，一个温暖、专业的情绪管理助手。
 现在你需要在共情用户的基础上，自然地引导用户进行情绪评估。
 请用1-2句话回应用户刚才说的内容，然后自然地过渡到："为了更好地帮助你，我想邀请你做一个简单的情绪评估。"

 重要规则：
 - 用简短、温暖的语言
 - 不要使用括号添加语气描述
 - 不要使用markdown格式符号"""

                ai_reply = llm_client.chat(
                    history_for_prompt, system_prompt=system_prompt
                )
                ai_reply = ai_reply.replace("**", "")
                ai_reply = clean_llm_response(ai_reply)

                # 保存AI回复
                ai_message_id = repo.save_message(
                    session_id=session.id,
                    role="assistant",
                    content=ai_reply,
                    message_type="text",
                )

                return ChatMessageResponse(
                    reply=ai_reply,
                    session_id=session.id,
                    message_id=ai_message_id,
                    requires_input=RequiresInputSchema(
                        type="emotion_images",
                        prompt="请选择最能代表你现在情绪的图片",
                        options=None,
                    ),
                )

        from app.agent.state import AgentState

        parsed_input = parse_user_input(request)

        intensity = parsed_input["intensity"]
        body_sensation = parsed_input["body_sensation"]
        image_emotion = parsed_input["image_emotion"]
        pending_image_urls = parsed_input["pending_image_urls"]

        # 状态管理：恢复已有状态或创建新状态
        graph = create_agent_graph(checkpointer=_checkpointer)
        config = {"configurable": {"thread_id": str(session.id)}}

        # 检查是否有已有状态
        try:
            checkpoint = graph.get_state(config)
            has_existing_state = (
                checkpoint and hasattr(checkpoint, "values") and checkpoint.values
            )
        except Exception:
            has_existing_state = False

        if has_existing_state:
            # 有已有状态，追加新消息
            current_state: AgentState = AgentState(**checkpoint.values)
            current_state["messages"] = list(current_state["messages"]) + [
                HumanMessage(content=request.message)
            ]

            # 更新各字段（如果本次选择了）
            if intensity is not None:
                current_state["intensity"] = intensity
                logger.info(f"更新强度: {intensity}")
                if current_state.get("current_emotion"):
                    current_state["current_emotion"]["intensity"] = intensity

            if body_sensation:
                current_state["body_sensation"] = body_sensation
                logger.info(f"更新身体感知: {body_sensation}")

            if image_emotion:
                current_state["image_emotion"] = {
                    "type": image_emotion,
                    "confidence": 0.9,
                    "reason": "用户选择的情绪图片",
                    "source": "image_selection",
                }
                logger.info(f"更新图片情绪: {image_emotion}")

            if pending_image_urls:
                current_state["pending_image_urls"] = pending_image_urls
                logger.info(f"设置待识别图片: {len(pending_image_urls)}张")

            logger.info(f"恢复已有状态，会话: {session.id}")
        else:
            # 无已有状态，创建新状态
            current_state = create_initial_state(session.id, user_id)
            current_state["messages"] = messages

            # 设置各字段（如果选择了）
            if intensity is not None:
                current_state["intensity"] = intensity
                if current_state.get("current_emotion"):
                    current_state["current_emotion"]["intensity"] = intensity

            if body_sensation:
                current_state["body_sensation"] = body_sensation

            if image_emotion:
                current_state["image_emotion"] = {
                    "type": image_emotion,
                    "confidence": 0.9,
                    "reason": "用户选择的情绪图片",
                    "source": "image_selection",
                }

            if pending_image_urls:
                current_state["pending_image_urls"] = pending_image_urls

            logger.info(f"创建新状态，会话: {session.id}")

        final_state = graph.invoke(current_state, config=config)

        ai_reply = ""
        for msg in reversed(final_state["messages"]):
            if isinstance(msg, AIMessage) and msg.content:
                ai_reply = msg.content
                break

        if not ai_reply:
            ai_reply = "我理解你的感受。能再多说一点你现在的情况吗？"

        ai_message_id = repo.save_message(
            session_id=session.id,
            role="assistant",
            content=ai_reply,
            message_type="text",
        )

        emotion = final_state.get("current_emotion")
        if emotion and isinstance(emotion, dict) and emotion.get("type"):
            repo.update_session(
                session.id,
                {
                    "initial_emotion_type": emotion.get("type"),
                    "initial_intensity": emotion.get("intensity"),
                    "is_crisis": final_state.get("is_crisis", False),
                },
            )

        logger.info(f"用户{user_id}发送消息到会话{session.id}")

        requires_input = None
        if final_state.get("requires_user_input"):
            next_action = final_state.get("next_action", "")
            if next_action == "wait_intensity_rating":
                requires_input = RequiresInputSchema(
                    type="intensity_slider",
                    prompt="请评估你当前的情绪强度",
                    options=None,
                )
            elif next_action == "wait_skill_confirmation":
                requires_input = RequiresInputSchema(
                    type="skill_confirmation",
                    prompt="你是否愿意尝试这个技能练习？",
                    options=["愿意", "再想想"],
                )
            elif next_action == "wait_step_completion":
                requires_input = RequiresInputSchema(
                    type="step_completion",
                    prompt="请完成当前步骤后告诉我你的感受",
                    options=None,
                )
            elif next_action == "body_sensation":
                requires_input = RequiresInputSchema(
                    type="body_selector",
                    prompt="请选择身体不适的部位",
                    options=None,
                )
            else:
                requires_input = RequiresInputSchema(
                    type="general", prompt="请继续输入", options=None
                )

        return ChatMessageResponse(
            reply=ai_reply,
            session_id=session.id,
            message_id=ai_message_id,
            requires_input=requires_input,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"发送消息失败: {str(e)}")
        raise HTTPException(
            status_code=500, detail={"code": 500, "message": "发送消息失败"}
        )


@router.post("/chat/message/multi-agent", response_model=ChatMessageResponse)
async def send_message_multi_agent(
    request: ChatMessageRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """
    发送对话消息（多AGENT协调器驱动）

    使用新的多AGENT架构：识别AGENT → 技能推荐AGENT → 干预引导AGENT
    支持状态持久化，保持对话连续性
    """
    try:
        repo = ChatRepository(db)

        if request.session_id:
            session = repo.get_session(request.session_id)
            if not session:
                raise HTTPException(
                    status_code=404, detail={"code": 404, "message": "会话不存在"}
                )
        else:
            session = repo.create_session(user_id)

        logger.info(f"用户{user_id}使用多AGENT发送消息到会话{session.id}")

        history_messages = repo.get_messages(session.id, limit=20)
        history_messages.reverse()

        messages = []
        for msg in history_messages:
            if msg.role == "user":
                messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                messages.append(AIMessage(content=msg.content))

        repo.save_message(
            session_id=session.id,
            role="user",
            content=request.message,
            message_type=request.message_type.value
            if hasattr(request.message_type, "value")
            else "text",
            metadata=request.metadata,
        )

        from app.agent.state import AgentState

        parsed_input = parse_user_input(request)

        intensity = parsed_input["intensity"]
        body_sensation = parsed_input["body_sensation"]
        image_emotion = parsed_input["image_emotion"]

        session_id_str = str(session.id)

        existing_state = repo.get_agent_state(session.id)
        if existing_state:
            current_state = existing_state
            logger.info(f"恢复已有状态，会话: {session_id_str}")
        else:
            current_state = create_initial_state(session_id_str, user_id)
            logger.info(f"创建新状态，会话: {session_id_str}")

        current_state["messages"] = messages

        if intensity is not None:
            current_state["intensity"] = intensity

        if body_sensation:
            current_state["body_sensation"] = body_sensation

        if image_emotion:
            current_state["image_emotion"] = {
                "type": image_emotion,
                "confidence": 0.9,
                "reason": "用户选择的情绪图片",
                "source": "image_selection",
            }

        logger.info(f"开始处理多AGENT对话，会话: {session_id_str}")

        result = await coordinator.process_conversation(request.message, current_state)

        ai_reply = result.get("response", "我理解你的感受。")

        if not isinstance(ai_reply, str):
            ai_reply = str(ai_reply) if ai_reply else "我理解你的感受。"

        ai_message_id = repo.save_message(
            session_id=session.id,
            role="assistant",
            content=ai_reply,
            message_type="text",
        )

        identified_emotion = result.get("identified_emotion")
        if identified_emotion and isinstance(identified_emotion, dict):
            repo.update_session(
                session.id,
                {
                    "initial_emotion_type": identified_emotion.get("type"),
                    "initial_intensity": identified_emotion.get("intensity"),
                    "is_crisis": result.get("is_crisis", False),
                },
            )

        updated_state = result.get("state", {})
        if updated_state:
            repo.update_agent_state(session.id, updated_state)

        requires_input = None
        next_action = (
            updated_state.get("next_action", "")
            if isinstance(updated_state, dict)
            else ""
        )

        if not result.get("should_end", True):
            if next_action == "wait_intensity_rating":
                requires_input = RequiresInputSchema(
                    type="intensity_slider",
                    prompt="请评估你当前的情绪强度",
                    options=None,
                )
            elif next_action == "wait_skill_confirmation":
                requires_input = RequiresInputSchema(
                    type="skill_confirmation",
                    prompt="你是否愿意尝试这个技能练习？",
                    options=["愿意", "再想想"],
                )
            elif next_action == "wait_step_completion":
                requires_input = RequiresInputSchema(
                    type="step_completion",
                    prompt="请完成当前步骤后告诉我你的感受",
                    options=None,
                )
            elif next_action == "body_sensation":
                requires_input = RequiresInputSchema(
                    type="body_selector",
                    prompt="请选择身体不适的部位",
                    options=None,
                )
            else:
                requires_input = RequiresInputSchema(
                    type="general", prompt="请继续输入", options=None
                )

        logger.info(f"多AGENT处理完成，会话: {session.id}")

        return ChatMessageResponse(
            reply=ai_reply,
            session_id=session.id,
            message_id=ai_message_id,
            requires_input=requires_input,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"多AGENT发送消息失败: {str(e)}")
        raise HTTPException(
            status_code=500, detail={"code": 500, "message": "发送消息失败"}
        )


@router.post("/chat/message/stream")
async def send_message_stream(
    request: ChatMessageRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """
    发送对话消息（流式输出）

    返回 Server-Sent Events (SSE) 流
    """
    try:
        repo = ChatRepository(db)

        if request.session_id:
            session = repo.get_session(request.session_id)
        else:
            session = repo.create_session(user_id)

        messages = [HumanMessage(content=request.message)]
        initial_state = create_initial_state(session.id, user_id)
        initial_state["messages"] = messages

        graph = create_agent_with_memory()

        async def generate():
            async for chunk in graph.astream(initial_state):
                for node_name, node_output in chunk.items():
                    if "messages" in node_output:
                        msgs = node_output["messages"]
                        for msg in msgs:
                            if isinstance(msg, AIMessage) and msg.content:
                                yield f"data: {msg.content}\n\n"
            yield "data: [DONE]\n\n"

        return generate()

    except Exception as e:
        logger.error(f"流式消息失败: {str(e)}")
        raise HTTPException(
            status_code=500, detail={"code": 500, "message": "发送消息失败"}
        )


@router.get("/chat/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    session_id: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """
    获取聊天历史
    """
    try:
        repo = ChatRepository(db)

        if not session_id:
            sessions, _ = repo.list_user_sessions(user_id, 1, 1)
            if not sessions:
                raise HTTPException(
                    status_code=404, detail={"code": 404, "message": "没有会话记录"}
                )
            session = sessions[0]
        else:
            session = repo.get_session(session_id)
            if not session:
                raise HTTPException(
                    status_code=404, detail={"code": 404, "message": "会话不存在"}
                )

        messages = repo.get_messages(session.id, limit)
        messages.reverse()

        message_items = []
        for msg in messages:
            metadata = json.loads(msg.extra_data) if msg.extra_data else None
            message_items.append(
                MessageItem(
                    role=msg.role,
                    content=msg.content,
                    created_at=msg.created_at,
                    metadata=metadata,
                )
            )

        emotion_change = None
        if (
            session.initial_intensity is not None
            and session.final_intensity is not None
        ):
            emotion_change = EmotionChange(
                initial_intensity=session.initial_intensity,
                final_intensity=session.final_intensity,
                improvement=session.initial_intensity - session.final_intensity,
            )

        return ChatHistoryResponse(
            session_id=session.id,
            start_time=session.start_time,
            end_time=session.end_time,
            status=session.status,
            messages=message_items,
            summary=session.summary,
            emotion_change=emotion_change,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取聊天历史失败: {str(e)}")
        raise HTTPException(
            status_code=500, detail={"code": 500, "message": "获取聊天历史失败"}
        )


@router.get("/chat/sessions", response_model=SessionListResponse)
async def list_sessions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """
    获取会话列表
    """
    try:
        repo = ChatRepository(db)

        sessions, total = repo.list_user_sessions(user_id, page, page_size)

        session_list = [
            SessionListItem(
                id=s.id,
                start_time=s.start_time,
                end_time=s.end_time,
                status=s.status,
                summary=s.summary,
                initial_emotion_type=s.initial_emotion_type,
            )
            for s in sessions
        ]

        return SessionListResponse(
            list=session_list, total=total, page=page, page_size=page_size
        )

    except Exception as e:
        logger.error(f"获取会话列表失败: {str(e)}")
        raise HTTPException(
            status_code=500, detail={"code": 500, "message": "获取会话列表失败"}
        )
