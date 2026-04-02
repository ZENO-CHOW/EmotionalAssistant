"""
危机事件数据访问层
"""

from sqlalchemy.orm import Session
from typing import Optional, List
import json
import uuid

from app.database.models import CrisisEvent


class CrisisRepository:
    """危机事件Repository"""

    def __init__(self, db: Session):
        self.db = db

    def create_crisis_event(self, crisis_data: dict) -> str:
        """创建危机事件"""
        event_id = str(uuid.uuid4())

        # 序列化JSON字段
        keywords_json = (
            json.dumps(crisis_data.get("detected_keywords"), ensure_ascii=False)
            if crisis_data.get("detected_keywords")
            else None
        )

        event = CrisisEvent(
            id=event_id,
            user_id=crisis_data["user_id"],
            session_id=crisis_data.get("session_id"),
            trigger_type=crisis_data["trigger_type"],
            trigger_reason=crisis_data["trigger_reason"],
            emotion_intensity=crisis_data["emotion_intensity"],
            detected_keywords=keywords_json,
            risk_level=crisis_data["risk_level"],
        )

        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)

        return event_id

    def get_crisis_event(self, event_id: str) -> Optional[CrisisEvent]:
        """获取危机事件详情"""
        return self.db.query(CrisisEvent).filter(CrisisEvent.id == event_id).first()

    def update_crisis_status(
        self, event_id: str, status: str, updates: dict = None
    ) -> bool:
        """更新危机事件状态"""
        event = self.get_crisis_event(event_id)
        if not event:
            return False

        event.status = status
        if updates:
            for key, value in updates.items():
                if hasattr(event, key):
                    setattr(event, key, value)

        self.db.commit()
        return True

    def list_user_crisis_events(self, user_id: int) -> List[CrisisEvent]:
        """查询用户危机事件列表"""
        return (
            self.db.query(CrisisEvent)
            .filter(CrisisEvent.user_id == user_id)
            .order_by(CrisisEvent.created_at.desc())
            .all()
        )

    def get_pending_crisis_count(self) -> int:
        """获取待处理危机事件数量"""
        return (
            self.db.query(CrisisEvent).filter(CrisisEvent.status == "pending").count()
        )

    def list_recent_crisis_events(
        self, limit: int = 10, status: str = None
    ) -> List[CrisisEvent]:
        """
        获取最近的危机事件列表
        :param limit: 返回数量限制
        :param status: 状态筛选 (pending/handling/resolved)
        :return: 危机事件列表
        """
        query = self.db.query(CrisisEvent).order_by(CrisisEvent.created_at.desc())

        if status:
            query = query.filter(CrisisEvent.status == status)

        return query.limit(limit).all()
