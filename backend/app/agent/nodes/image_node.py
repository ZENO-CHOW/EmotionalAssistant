"""
图片情绪识别节点
"""

import logging
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from langchain_core.messages import AIMessage
from app.agent.state import AgentState
from app.core.vision_client import get_vision_client
from app.utils.image_utils import load_image_as_data_url

logger = logging.getLogger(__name__)


def image_recognition_node(
    state: AgentState, db: Optional[Session] = None
) -> AgentState:
    """
    图片识别节点

    处理用户上传的图片，识别情绪并更新状态
    支持多张图片批量识别，最后汇总结果

    Args:
        state: AgentState
        db: 数据库会话

    Returns:
        更新后的 AgentState
    """
    pending_urls = state.get("pending_image_urls")
    if not pending_urls or len(pending_urls) == 0:
        return state

    logger.info(f"开始识别图片情绪，共 {len(pending_urls)} 张图片")

    vision_client = get_vision_client()
    emotion_results = []

    for idx, url in enumerate(pending_urls):
        logger.info(f"识别第 {idx + 1}/{len(pending_urls)} 张图片: {url}")

        try:
            data_url = load_image_as_data_url(url)
            emotion_result = vision_client.recognize_emotion(data_url)
        except FileNotFoundError as e:
            logger.warning(f"第 {idx + 1} 张图片文件不存在: {e}")
            continue
        except Exception as e:
            logger.warning(f"第 {idx + 1} 张图片处理失败: {e}")
            continue

        if not emotion_result:
            logger.warning(f"第 {idx + 1} 张图片识别返回空结果")
            continue

        emotion_results.append(
            {
                "type": emotion_result.get("emotion_type", "calm"),
                "confidence": emotion_result.get("confidence", 0.5),
                "reason": emotion_result.get("reason", ""),
                "image_url": url,
            }
        )

    if not emotion_results:
        logger.warning("所有图片识别均失败")

        attempts = state.get("image_recognition_attempts", 0)

        if attempts < 2:
            state["image_recognition_attempts"] = attempts + 1
            state["requires_user_input"] = True
            state["next_action"] = "image_recognition_failed"
            state["messages"] = list(state["messages"]) + [
                AIMessage(
                    content="抱歉，我没能看清这些图片。你可以重新选择，或者用文字告诉我你现在的心情吗？"
                )
            ]
            return state
        else:
            state["pending_image_urls"] = None
            state["image_recognition_attempts"] = 0
            logger.warning("图片识别重试次数已达上限，跳过识别")
            return state

    logger.info(f"成功识别 {len(emotion_results)} 张图片")

    emotion_counts: Dict[str, int] = {}
    total_confidence: Dict[str, float] = {}
    all_reasons: list[str] = []

    for result in emotion_results:
        emotion_type = result["type"]
        emotion_counts[emotion_type] = emotion_counts.get(emotion_type, 0) + 1
        total_confidence[emotion_type] = (
            total_confidence.get(emotion_type, 0) + result["confidence"]
        )
        all_reasons.append(result["reason"])

    dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0]
    dominant_count = emotion_counts[dominant_emotion]
    avg_confidence = total_confidence[dominant_emotion] / dominant_count

    unique_reasons = list(set(all_reasons))[:3]
    combined_reason = " ".join(unique_reasons) if unique_reasons else ""

    img_emotion: Dict[str, Any] = {
        "type": dominant_emotion,
        "confidence": avg_confidence,
        "reason": combined_reason,
        "source": "image_recognition",
        "details": emotion_results,
        "total_images": len(pending_urls),
        "recognized_images": len(emotion_results),
    }
    state["image_emotion"] = img_emotion

    current_emotion: Dict[str, Any] = state.get("current_emotion") or {}
    current_emotion["type"] = img_emotion.get("type", "calm")
    current_emotion["confidence"] = img_emotion.get("confidence", 0.5)
    current_emotion["reason"] = img_emotion.get("reason", "")
    current_emotion["source"] = "image"
    state["current_emotion"] = current_emotion

    state["pending_image_urls"] = None
    state["image_recognition_attempts"] = 0

    emotion_map = {
        "joy": "开心",
        "calm": "平静",
        "sadness": "难过",
        "anxiety": "焦虑",
        "anger": "愤怒",
        "fear": "害怕",
    }
    image_emotion_type = img_emotion.get("type", "calm")
    emotion_cn = emotion_map.get(image_emotion_type, image_emotion_type)

    if len(emotion_results) > 1:
        feedback = f"从你选择的 {len(emotion_results)} 张图片中，我感受到你可能有些{emotion_cn}。"
    else:
        feedback = f"从你选择的图片中，我感受到你可能有些{emotion_cn}。"

    if combined_reason:
        feedback += f" {combined_reason}"

    state["messages"] = list(state["messages"]) + [AIMessage(content=feedback)]

    logger.info(f"图片识别完成: {img_emotion}")

    return state
