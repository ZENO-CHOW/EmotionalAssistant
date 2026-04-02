"""
情绪图片API路由
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
import random
import logging

from app.database.connection import get_db
from app.database.models import EmotionImage

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/emotion/images")
async def get_emotion_images(
    category: Optional[str] = Query(
        None, description="图片分类: positive/negative/neutral"
    ),
    limit: int = Query(12, ge=1, le=50, description="返回数量"),
    random_select: bool = Query(True, description="是否随机选择"),
    db: Session = Depends(get_db),
):
    """
    获取情绪图片列表

    用于让用户选择符合当前感受的图片
    """
    try:
        # 构建查询
        query = db.query(EmotionImage)

        # 按分类筛选
        if category:
            if category not in ["positive", "negative", "neutral"]:
                raise HTTPException(status_code=400, detail="无效的分类")
            query = query.filter(EmotionImage.category == category)

        # 获取所有符合条件的图片
        all_images = query.all()

        if not all_images:
            return {"success": True, "count": 0, "images": []}

        # 随机选择或按顺序选择
        if random_select:
            selected = random.sample(all_images, min(limit, len(all_images)))
        else:
            selected = all_images[:limit]

        # 格式化返回数据
        images = [
            {
                "imageId": img.image_id,
                "url": img.file_path,
                "category": img.category,
                "name": img.name,
                "valence": img.valence,
                "arousal": img.arousal,
                "dominance": img.dominance,
            }
            for img in selected
        ]

        return {
            "success": True,
            "count": len(images),
            "category": category,
            "images": images,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取图片列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取图片列表失败: {str(e)}")


@router.post("/emotion/analyze")
async def analyze_emotion(data: dict, db: Session = Depends(get_db)):
    """
    分析用户选择的图片，识别情绪

    基于用户选择的图片VAD值计算情绪类型
    """
    try:
        selected_images = data.get("selectedImages", [])
        intensity = data.get("intensity", 5)

        if not selected_images:
            raise HTTPException(status_code=400, detail="未选择图片")

        # 获取选中图片的VAD值
        image_ids = [img.get("imageId") for img in selected_images]
        images = (
            db.query(EmotionImage).filter(EmotionImage.image_id.in_(image_ids)).all()
        )

        if not images:
            raise HTTPException(status_code=404, detail="未找到图片数据")

        # 计算平均VAD值
        valence_sum = sum(float(img.valence) for img in images)  # type: ignore[arg-type]
        arousal_sum = sum(float(img.arousal) for img in images)  # type: ignore[arg-type]
        dominance_sum = sum(float(img.dominance) for img in images)  # type: ignore[arg-type]
        avg_valence = valence_sum / len(images)
        avg_arousal = arousal_sum / len(images)
        avg_dominance = dominance_sum / len(images)

        # 根据VAD映射到情绪类型
        emotion_result = map_vad_to_emotion(
            avg_valence, avg_arousal, avg_dominance, intensity
        )

        return {
            "success": True,
            "emotion": emotion_result,
            "vad": {
                "valence": round(avg_valence, 2),
                "arousal": round(avg_arousal, 2),
                "dominance": round(avg_dominance, 2),
            },
            "intensity": intensity,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"情绪分析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"情绪分析失败: {str(e)}")


def map_vad_to_emotion(
    valence: float, arousal: float, dominance: float, intensity: int
) -> dict:
    """
    将VAD值映射到情绪类型

    基于效价（Valence）、唤醒度（Arousal）、支配度（Dominance）
    """
    # 简化的情绪映射规则
    if valence < 4.5:  # 低效价（负面）
        if arousal > 5.5:  # 高唤醒
            if dominance < 5.0:
                emotion_type = "anxiety"
                emotion_label = "焦虑"
                emoji = "😰"
            else:
                emotion_type = "anger"
                emotion_label = "愤怒"
                emoji = "😠"
        else:  # 低唤醒
            emotion_type = "sadness"
            emotion_label = "悲伤"
            emoji = "😢"
    elif valence > 5.5:  # 高效价（正面）
        if arousal > 5.5:  # 高唤醒
            emotion_type = "joy"
            emotion_label = "快乐"
            emoji = "😊"
        else:  # 低唤醒
            emotion_type = "calm"
            emotion_label = "平静"
            emoji = "😌"
    else:  # 中性效价
        emotion_type = "neutral"
        emotion_label = "中性"
        emoji = "😐"

    return {
        "emotionType": emotion_type,
        "emotionLabel": emotion_label,
        "emoji": emoji,
        "intensity": intensity,
        "confidence": 0.75,  # 简化版，固定置信度
        "description": f"看起来你现在可能感到{emotion_label}",
    }


@router.get("/emotion/images/statistics")
async def get_image_statistics(db: Session = Depends(get_db)):
    """
    获取图片库统计信息
    """
    try:
        positive_count = (
            db.query(EmotionImage).filter(EmotionImage.category == "positive").count()
        )
        negative_count = (
            db.query(EmotionImage).filter(EmotionImage.category == "negative").count()
        )
        neutral_count = (
            db.query(EmotionImage).filter(EmotionImage.category == "neutral").count()
        )

        return {
            "success": True,
            "total": positive_count + negative_count + neutral_count,
            "categories": {
                "positive": positive_count,
                "negative": negative_count,
                "neutral": neutral_count,
            },
        }

    except Exception as e:
        logger.error(f"获取统计失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取统计失败: {str(e)}")
