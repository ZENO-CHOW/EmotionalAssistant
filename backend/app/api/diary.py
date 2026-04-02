"""
情绪日记API路由
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date, datetime, timedelta
import json
import logging

from app.database.connection import get_db
from app.database.repositories.diary_repo import DiaryRepository
from app.database.repositories.chat_repo import ChatRepository
from app.models.diary import (
    CreateDiaryRequest,
    UpdateDiaryRequest,
    DiaryResponse,
    DiaryListResponse,
    EmotionStatisticsResponse,
    TrendPoint,
)
from app.core.dependencies import get_current_user_id
from app.core.llm_client import LLMClient
from app.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


def parse_diary_response(diary) -> dict:
    """解析日记数据，反序列化JSON字段，兼容前端字段名"""
    data = {
        "id": diary.id,
        "user_id": diary.user_id,
        "emotion_type": diary.emotion_type,
        "emotion_label": diary.emotion_label,
        "emotion": diary.emotion_type,  # 兼容前端
        "emotionLabel": diary.emotion_label,  # 兼容前端
        "emoji": diary.emoji,
        "intensity": diary.intensity,
        "content": diary.content,
        "triggers": json.loads(diary.triggers) if diary.triggers else None,
        "body_parts": json.loads(diary.body_parts) if diary.body_parts else None,
        "selected_images": json.loads(diary.selected_images)
        if diary.selected_images
        else None,
        "created_at": diary.created_at.isoformat()
        if isinstance(diary.created_at, datetime)
        else diary.created_at,
        "updated_at": diary.updated_at.isoformat()
        if isinstance(diary.updated_at, datetime)
        else diary.updated_at,
        "diary_date": diary.diary_date.isoformat()
        if isinstance(diary.diary_date, (date, datetime))
        else diary.diary_date,
    }
    return data


@router.post("/diary", response_model=DiaryResponse)
async def create_diary(
    request: CreateDiaryRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """
    创建情绪日记
    """
    try:
        repo = DiaryRepository(db)

        # 检查当天是否已有日记
        diary_date = request.diary_date or date.today().isoformat()
        if repo.check_diary_exists(user_id, diary_date):
            raise HTTPException(
                status_code=409, detail={"code": 409, "message": "当天已有日记"}
            )

        # 准备日记数据（转换字段名）
        diary_data = request.model_dump()
        if "emotion" in diary_data:
            if diary_data["emotion"]:
                diary_data["emotion_type"] = diary_data["emotion"]
            del diary_data["emotion"]
        if "emotionLabel" in diary_data:
            if diary_data["emotionLabel"]:
                diary_data["emotion_label"] = diary_data["emotionLabel"]
            del diary_data["emotionLabel"]
        diary_data["diary_date"] = diary_date

        # 创建日记
        diary_id = repo.create_diary(user_id, diary_data)

        # 获取创建的日记
        diary = repo.get_diary(diary_id, user_id)

        logger.info(f"用户{user_id}创建日记: {diary_id}")
        return DiaryResponse(**parse_diary_response(diary))

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"创建日记失败: {str(e)}")
        raise HTTPException(
            status_code=500, detail={"code": 500, "message": "创建日记失败"}
        )


@router.get("/diary/list", response_model=DiaryListResponse)
async def list_diaries(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    emotion_type: Optional[str] = None,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """
    获取日记列表
    """
    try:
        repo = DiaryRepository(db)

        # 构建过滤条件
        filters = {}
        if start_date:
            filters["start_date"] = start_date
        if end_date:
            filters["end_date"] = end_date
        if emotion_type:
            filters["emotion_type"] = emotion_type

        # 查询日记列表
        diaries, total = repo.list_diaries(user_id, filters, page, page_size)

        # 解析数据
        diary_list = [DiaryResponse(**parse_diary_response(d)) for d in diaries]

        return DiaryListResponse(
            list=diary_list,
            total=total,
            page=page,
            page_size=page_size,
            has_more=total > page * page_size,
        )

    except Exception as e:
        logger.error(f"获取日记列表失败: {str(e)}")
        raise HTTPException(
            status_code=500, detail={"code": 500, "message": "获取日记列表失败"}
        )


@router.get("/diary/{diary_id}", response_model=DiaryResponse)
async def get_diary(
    diary_id: str,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """
    获取日记详情
    """
    try:
        repo = DiaryRepository(db)
        diary = repo.get_diary(diary_id, user_id)

        if not diary:
            raise HTTPException(
                status_code=404, detail={"code": 404, "message": "日记不存在"}
            )

        return DiaryResponse(**parse_diary_response(diary))

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取日记详情失败: {str(e)}")
        raise HTTPException(
            status_code=500, detail={"code": 500, "message": "获取日记详情失败"}
        )


@router.put("/diary/{diary_id}", response_model=DiaryResponse)
async def update_diary(
    diary_id: str,
    request: UpdateDiaryRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """
    更新日记
    """
    try:
        repo = DiaryRepository(db)

        # 检查日记是否存在
        diary = repo.get_diary(diary_id, user_id)
        if not diary:
            raise HTTPException(
                status_code=404, detail={"code": 404, "message": "日记不存在"}
            )

        # 准备更新数据（转换字段名）
        updates = request.model_dump(exclude_unset=True)
        if "emotion" in updates:
            if updates["emotion"]:
                updates["emotion_type"] = updates["emotion"]
            del updates["emotion"]
        if "emotionLabel" in updates:
            if updates["emotionLabel"]:
                updates["emotion_label"] = updates["emotionLabel"]
            del updates["emotionLabel"]

        # 更新日记
        success = repo.update_diary(diary_id, user_id, updates)
        if not success:
            raise HTTPException(
                status_code=500, detail={"code": 500, "message": "更新日记失败"}
            )

        # 获取更新后的日记
        diary = repo.get_diary(diary_id, user_id)

        logger.info(f"用户{user_id}更新日记: {diary_id}")
        return DiaryResponse(**parse_diary_response(diary))

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新日记失败: {str(e)}")
        raise HTTPException(
            status_code=500, detail={"code": 500, "message": "更新日记失败"}
        )


@router.delete("/diary/{diary_id}")
async def delete_diary(
    diary_id: str,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """
    删除日记
    """
    try:
        repo = DiaryRepository(db)

        success = repo.delete_diary(diary_id, user_id)
        if not success:
            raise HTTPException(
                status_code=404, detail={"code": 404, "message": "日记不存在"}
            )

        logger.info(f"用户{user_id}删除日记: {diary_id}")
        return {"code": 200, "message": "删除成功"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除日记失败: {str(e)}")
        raise HTTPException(
            status_code=500, detail={"code": 500, "message": "删除日记失败"}
        )


@router.get("/diary/today", response_model=DiaryResponse | None)
async def get_today_diary(
    db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)
):
    """
    获取今日日记
    """
    try:
        repo = DiaryRepository(db)
        diary = repo.get_today_diary(user_id)

        if not diary:
            return None

        return DiaryResponse(**parse_diary_response(diary))

    except Exception as e:
        logger.error(f"获取今日日记失败: {str(e)}")
        raise HTTPException(
            status_code=500, detail={"code": 500, "message": "获取今日日记失败"}
        )


@router.get("/emotion/statistics", response_model=EmotionStatisticsResponse)
async def get_emotion_statistics(
    time_range: str = Query("week", pattern="^(week|month|quarter|year)$"),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """
    获取情绪统计
    """
    try:
        repo = DiaryRepository(db)

        # 计算时间范围
        end_date = date.today()
        days_map = {"week": 7, "month": 30, "quarter": 90, "year": 365}
        start_date = end_date - timedelta(days=days_map[time_range])

        start_str = start_date.isoformat()
        end_str = end_date.isoformat()

        # 统计数据
        diaries, total = repo.list_diaries(
            user_id, {"start_date": start_str, "end_date": end_str}, 1, 9999
        )
        continuous_days = repo.get_continuous_days(user_id)
        distribution = repo.get_emotion_distribution(user_id, start_str, end_str)
        average_intensity = repo.get_average_intensity(user_id, start_str, end_str)
        trend_data = repo.get_trend_data(user_id, days_map[time_range])

        # 找出最常见情绪
        most_common = (
            max(distribution.items(), key=lambda x: x[1])[0] if distribution else None
        )

        return EmotionStatisticsResponse(
            total_records=total,
            continuous_days=continuous_days,
            emotion_distribution=distribution,
            average_intensity=average_intensity,
            most_common_emotion=most_common,
            trend_data=[TrendPoint(**t) for t in trend_data],
        )

    except Exception as e:
        logger.error(f"获取情绪统计失败: {str(e)}")
        raise HTTPException(
            status_code=500, detail={"code": 500, "message": "获取情绪统计失败"}
        )


@router.get("/emotion/trend")
async def get_emotion_trend(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """
    获取情绪趋势
    """
    try:
        repo = DiaryRepository(db)
        trend_data = repo.get_trend_data(user_id, days)

        return trend_data

    except Exception as e:
        logger.error(f"获取情绪趋势失败: {str(e)}")
        raise HTTPException(
            status_code=500, detail={"code": 500, "message": "获取情绪趋势失败"}
        )
