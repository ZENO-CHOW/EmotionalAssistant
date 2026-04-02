"""
对话数据访问层
"""

from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, func
from typing import Optional, List
from datetime import datetime, timedelta
import json
import uuid

from app.database.models import ChatSession, ChatMessage


class ChatRepository:
    """对话Repository"""

    def __init__(self, db: Session):
        self.db = db

    def create_session(self, user_id: int) -> ChatSession:
        """创建新会话"""
        session_id = str(uuid.uuid4())
        session = ChatSession(id=session_id, user_id=user_id, status="active")
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """获取会话详情"""
        return self.db.query(ChatSession).filter(ChatSession.id == session_id).first()

    def update_session(self, session_id: str, updates: dict) -> bool:
        """更新会话信息"""
        session = self.get_session(session_id)
        if not session:
            return False

        # 序列化JSON字段
        if "recommended_skills" in updates and updates["recommended_skills"]:
            updates["recommended_skills"] = json.dumps(
                updates["recommended_skills"], ensure_ascii=False
            )

        for key, value in updates.items():
            if hasattr(session, key):
                setattr(session, key, value)

        self.db.commit()
        return True

    def list_user_sessions(
        self, user_id: int, page: int = 1, page_size: int = 20
    ) -> tuple[List[ChatSession], int]:
        """查询用户会话列表"""
        query = self.db.query(ChatSession).filter(ChatSession.user_id == user_id)
        total = query.count()

        sessions = (
            query.order_by(desc(ChatSession.start_time))
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return sessions, total

    def save_message(
        self,
        session_id: str,
        role: str,
        content: str,
        message_type: str = "text",
        metadata: dict = None,
    ) -> int:
        """保存消息"""
        metadata_json = json.dumps(metadata, ensure_ascii=False) if metadata else None

        message = ChatMessage(
            session_id=session_id,
            role=role,
            content=content,
            message_type=message_type,
            metadata=metadata_json,
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message.id

    def get_messages(self, session_id: str, limit: int = 20) -> List[ChatMessage]:
        """获取会话消息"""
        return (
            self.db.query(ChatMessage)
            .filter(ChatMessage.session_id == session_id)
            .order_by(desc(ChatMessage.created_at))
            .limit(limit)
            .all()
        )

    def get_recent_high_intensity_count(
        self, user_id: int, days: int = 7, threshold: int = 8
    ) -> int:
        """统计近期高强度情绪次数（用于危机检测）"""
        from app.database.models import SkillUsageRecord

        start_date = datetime.now() - timedelta(days=days)
        count = (
            self.db.query(SkillUsageRecord)
            .filter(
                and_(
                    SkillUsageRecord.user_id == user_id,
                    SkillUsageRecord.before_intensity > threshold,
                    SkillUsageRecord.created_at >= start_date,
                )
            )
            .count()
        )

        return count

    def get_agent_state(self, session_id: str) -> Optional[dict]:
        """获取会话的多AGENT状态"""
        session = self.get_session(session_id)
        if not session or not session.agent_state:
            return None
        try:
            return json.loads(session.agent_state)
        except (json.JSONDecodeError, TypeError):
            return None

    def update_agent_state(self, session_id: str, state: dict) -> bool:
        """保存会话的多AGENT状态"""
        session = self.get_session(session_id)
        if not session:
            return False

        try:
            session.agent_state = json.dumps(state, ensure_ascii=False)
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False
