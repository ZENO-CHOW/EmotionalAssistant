"""
情绪日记数据访问层
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from typing import Optional, List, Tuple, Dict, Any
from datetime import datetime, date, timedelta
import json
import uuid

from app.database.models import EmotionDiary
from app.config import settings


class DiaryRepository:
    """情绪日记Repository"""

    def __init__(self, db: Session):
        self.db = db

    def create_diary(self, user_id: int, diary_data: dict) -> str:
        """
        创建日记
        :param user_id: 用户ID
        :param diary_data: 日记数据
        :return: 日记ID
        """
        diary_id = str(uuid.uuid4())
        diary_date = diary_data.get("diary_date") or date.today().isoformat()

        # 序列化JSON字段
        triggers_json = (
            json.dumps(diary_data.get("triggers"), ensure_ascii=False)
            if diary_data.get("triggers")
            else None
        )
        body_parts_json = (
            json.dumps(diary_data.get("body_parts"), ensure_ascii=False)
            if diary_data.get("body_parts")
            else None
        )
        images_json = (
            json.dumps(diary_data.get("selected_images"), ensure_ascii=False)
            if diary_data.get("selected_images")
            else None
        )

        diary = EmotionDiary(
            id=diary_id,
            user_id=user_id,
            emotion_type=diary_data["emotion_type"],
            emotion_label=diary_data["emotion_label"],
            emoji=diary_data["emoji"],
            intensity=diary_data["intensity"],
            content=diary_data.get("content"),
            triggers=triggers_json,
            body_parts=body_parts_json,
            selected_images=images_json,
            diary_date=datetime.strptime(diary_date, "%Y-%m-%d").date(),
        )

        self.db.add(diary)
        self.db.commit()
        self.db.refresh(diary)

        return diary_id

    def get_diary(
        self, diary_id: str, user_id: Optional[int] = None
    ) -> Optional[EmotionDiary]:
        """
        获取日记详情
        :param diary_id: 日记ID
        :param user_id: 用户ID（用于权限校验）
        :return: 日记对象
        """
        query = self.db.query(EmotionDiary).filter(EmotionDiary.id == diary_id)
        if user_id:
            query = query.filter(EmotionDiary.user_id == user_id)
        return query.first()

    def update_diary(self, diary_id: str, user_id: int, updates: dict) -> bool:
        """
        更新日记
        :param diary_id: 日记ID
        :param user_id: 用户ID
        :param updates: 更新数据
        :return: 是否成功
        """
        diary = self.get_diary(diary_id, user_id)
        if not diary:
            return False

        # 处理需要序列化的字段
        if "triggers" in updates and updates["triggers"] is not None:
            updates["triggers"] = json.dumps(updates["triggers"], ensure_ascii=False)
        if "body_parts" in updates and updates["body_parts"] is not None:
            updates["body_parts"] = json.dumps(
                updates["body_parts"], ensure_ascii=False
            )
        if "selected_images" in updates and updates["selected_images"] is not None:
            updates["selected_images"] = json.dumps(
                updates["selected_images"], ensure_ascii=False
            )

        # 更新字段
        for key, value in updates.items():
            if value is not None and hasattr(diary, key):
                setattr(diary, key, value)

        diary.updated_at = datetime.now()  # type: ignore
        self.db.commit()
        return True

    def delete_diary(self, diary_id: str, user_id: int) -> bool:
        """
        删除日记
        :param diary_id: 日记ID
        :param user_id: 用户ID
        :return: 是否成功
        """
        diary = self.get_diary(diary_id, user_id)
        if not diary:
            return False

        self.db.delete(diary)
        self.db.commit()
        return True

    def list_diaries(
        self,
        user_id: int,
        filters: Optional[Dict[str, Any]] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Tuple[List[EmotionDiary], int]:
        """
        查询日记列表
        :param user_id: 用户ID
        :param filters: 过滤条件（start_date, end_date, emotion_type）
        :param page: 页码
        :param page_size: 每页数量
        :return: (日记列表, 总数)
        """
        query = self.db.query(EmotionDiary).filter(EmotionDiary.user_id == user_id)

        # 应用过滤条件
        if filters:
            if filters.get("start_date"):
                start_date = datetime.strptime(filters["start_date"], "%Y-%m-%d").date()
                query = query.filter(EmotionDiary.diary_date >= start_date)
            if filters.get("end_date"):
                end_date = datetime.strptime(filters["end_date"], "%Y-%m-%d").date()
                query = query.filter(EmotionDiary.diary_date <= end_date)
            if filters.get("emotion_type"):
                query = query.filter(
                    EmotionDiary.emotion_type == filters["emotion_type"]
                )

        # 统计总数
        total = query.count()

        # 分页查询
        query = query.order_by(desc(EmotionDiary.diary_date))
        diaries = query.offset((page - 1) * page_size).limit(page_size).all()

        return diaries, total

    def get_today_diary(
        self, user_id: int, diary_date: Optional[str] = None
    ) -> Optional[EmotionDiary]:
        """
        获取指定日期的日记
        :param user_id: 用户ID
        :param diary_date: 日记日期（默认今天）
        :return: 日记对象
        """
        if diary_date is None:
            diary_date = date.today().isoformat()

        target_date = datetime.strptime(diary_date, "%Y-%m-%d").date()
        return (
            self.db.query(EmotionDiary)
            .filter(
                and_(
                    EmotionDiary.user_id == user_id,
                    EmotionDiary.diary_date == target_date,
                )
            )
            .first()
        )

    def check_diary_exists(self, user_id: int, diary_date: str) -> bool:
        """
        检查日期是否已有日记
        :param user_id: 用户ID
        :param diary_date: 日记日期
        :return: 是否存在
        """
        target_date = datetime.strptime(diary_date, "%Y-%m-%d").date()
        count = (
            self.db.query(EmotionDiary)
            .filter(
                and_(
                    EmotionDiary.user_id == user_id,
                    EmotionDiary.diary_date == target_date,
                )
            )
            .count()
        )
        return count > 0

    def get_continuous_days(self, user_id: int) -> int:
        """
        计算连续打卡天数
        :param user_id: 用户ID
        :return: 连续天数
        """
        # 获取所有日记日期，按日期降序
        dates = (
            self.db.query(EmotionDiary.diary_date)
            .filter(EmotionDiary.user_id == user_id)
            .order_by(desc(EmotionDiary.diary_date))
            .all()
        )

        if not dates:
            return 0

        dates = [d[0] for d in dates]
        today = date.today()
        continuous_days = 0

        # 从今天往前检查
        current_date = today
        for diary_date in dates:
            if diary_date == current_date:
                continuous_days += 1
                current_date = current_date - timedelta(days=1)
            elif diary_date < current_date:
                # 如果跳过了某一天，中断计数
                break

        return continuous_days

    def get_emotion_distribution(
        self,
        user_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, int]:
        """
        统计情绪分布
        :param user_id: 用户ID
        :param start_date: 开始日期
        :param end_date: 结束日期
        :return: 情绪分布字典
        """
        query = self.db.query(
            EmotionDiary.emotion_type, func.count(EmotionDiary.id).label("count")
        ).filter(EmotionDiary.user_id == user_id)

        if start_date:
            query = query.filter(
                EmotionDiary.diary_date
                >= datetime.strptime(start_date, "%Y-%m-%d").date()
            )
        if end_date:
            query = query.filter(
                EmotionDiary.diary_date
                <= datetime.strptime(end_date, "%Y-%m-%d").date()
            )

        results = query.group_by(EmotionDiary.emotion_type).all()

        # 初始化所有情绪类型
        distribution = {
            "joy": 0,
            "calm": 0,
            "sadness": 0,
            "anxiety": 0,
            "anger": 0,
            "fear": 0,
        }

        for emotion_type, count in results:
            distribution[emotion_type] = count

        return distribution

    def get_average_intensity(
        self,
        user_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> float:
        """
        计算平均情绪强度
        :param user_id: 用户ID
        :param start_date: 开始日期
        :param end_date: 结束日期
        :return: 平均强度
        """
        query = self.db.query(func.avg(EmotionDiary.intensity)).filter(
            EmotionDiary.user_id == user_id
        )

        if start_date:
            query = query.filter(
                EmotionDiary.diary_date
                >= datetime.strptime(start_date, "%Y-%m-%d").date()
            )
        if end_date:
            query = query.filter(
                EmotionDiary.diary_date
                <= datetime.strptime(end_date, "%Y-%m-%d").date()
            )

        result = query.scalar()
        return round(float(result), 2) if result else 0.0

    def get_trend_data(self, user_id: int, days: int = 30) -> List[dict]:
        """
        获取趋势数据
        :param user_id: 用户ID
        :param days: 天数
        :return: 趋势数据列表
        """
        end_date = date.today()
        start_date = end_date - timedelta(days=days - 1)

        # 查询数据
        results = (
            self.db.query(
                EmotionDiary.diary_date,
                func.avg(EmotionDiary.intensity).label("avg_intensity"),
                func.count(EmotionDiary.id).label("count"),
            )
            .filter(
                and_(
                    EmotionDiary.user_id == user_id,
                    EmotionDiary.diary_date >= start_date,
                    EmotionDiary.diary_date <= end_date,
                )
            )
            .group_by(EmotionDiary.diary_date)
            .all()
        )

        # 创建日期映射
        data_map = {
            str(r.diary_date): {
                "average_intensity": round(float(r.avg_intensity), 2),
                "record_count": r.count,
            }
            for r in results
        }

        # 填充完整时间序列
        trend_data = []
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.isoformat()
            if date_str in data_map:
                trend_data.append({"date": date_str, **data_map[date_str]})
            else:
                trend_data.append(
                    {"date": date_str, "average_intensity": None, "record_count": 0}
                )
            current_date += timedelta(days=1)

        return trend_data

    def get_total_diary_count(self) -> int:
        """获取情绪日记总数"""
        return self.db.query(EmotionDiary).count()

    def get_global_emotion_distribution(
        self, start_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> List[Dict]:
        """
        统计全局情绪分布（所有用户）
        :param start_date: 开始日期 (YYYY-MM-DD)
        :param end_date: 结束日期 (YYYY-MM-DD)
        :return: 情绪分布列表
        """
        query = self.db.query(
            EmotionDiary.emotion_type, func.count(EmotionDiary.id).label("count")
        )

        if start_date:
            query = query.filter(
                EmotionDiary.diary_date
                >= datetime.strptime(start_date, "%Y-%m-%d").date()
            )
        if end_date:
            query = query.filter(
                EmotionDiary.diary_date
                <= datetime.strptime(end_date, "%Y-%m-%d").date()
            )

        results = query.group_by(EmotionDiary.emotion_type).all()

        emotion_config = {
            "joy": {
                "emoji": "😊",
                "name": "开心",
                "color": "linear-gradient(135deg, #10b981, #34d399)",
            },
            "calm": {
                "emoji": "😌",
                "name": "平静",
                "color": "linear-gradient(135deg, #6b7280, #9ca3af)",
            },
            "sadness": {
                "emoji": "😢",
                "name": "难过",
                "color": "linear-gradient(135deg, #3b82f6, #60a5fa)",
            },
            "anxiety": {
                "emoji": "😰",
                "name": "焦虑",
                "color": "linear-gradient(135deg, #f59e0b, #f97316)",
            },
            "anger": {
                "emoji": "😠",
                "name": "生气",
                "color": "linear-gradient(135deg, #ef4444, #f87171)",
            },
            "fear": {
                "emoji": "😨",
                "name": "恐惧",
                "color": "linear-gradient(135deg, #8b5cf6, #a78bfa)",
            },
        }

        total_count = sum(count for _, count in results) if results else 0

        distribution = []
        for emotion_type, count in results:
            if emotion_type in emotion_config:
                config = emotion_config[emotion_type]
                distribution.append(
                    {
                        "type": emotion_type,
                        "emoji": config["emoji"],
                        "name": config["name"],
                        "count": count,
                        "percentage": round((count / total_count * 100), 1)
                        if total_count > 0
                        else 0,
                        "color": config["color"],
                    }
                )

        return distribution
