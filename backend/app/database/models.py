"""
数据库模型定义
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    ForeignKey,
    Index,
    Date,
    Float,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional
from app.database.connection import Base


class User(Base):
    """用户表"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    nickname: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(
        String(100), unique=True, nullable=True, index=True
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    school: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    avatar: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class ChatSession(Base):
    """对话会话表"""

    __tablename__ = "chat_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    start_time: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    initial_emotion_type: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True
    )
    initial_intensity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    final_intensity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    recommended_skills: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_crisis: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    assessment_status: Mapped[str] = mapped_column(
        String(20), default="not_started", nullable=False
    )
    assessment_data: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    agent_state: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    __table_args__ = (Index("idx_user_start_time", "user_id", "start_time"),)


class ChatMessage(Base):
    """对话消息表"""

    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    session_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    message_type: Mapped[str] = mapped_column(
        String(30), default="text", nullable=False
    )
    extra_data: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )

    __table_args__ = (Index("idx_session_created", "session_id", "created_at"),)


class EmotionDiary(Base):
    """情绪日记表"""

    __tablename__ = "emotion_diaries"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    emotion_type: Mapped[str] = mapped_column(String(50), nullable=False)
    emotion_label: Mapped[str] = mapped_column(String(50), nullable=False)
    emoji: Mapped[str] = mapped_column(String(10), nullable=False)
    intensity: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    triggers: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    body_parts: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    selected_images: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
    diary_date: Mapped[datetime] = mapped_column(Date, nullable=False, index=True)

    __table_args__ = (
        Index("idx_user_diary_date", "user_id", "diary_date", unique=True),
        Index("idx_user_created", "user_id", "created_at"),
    )


class SkillUsageRecord(Base):
    """DBT技能使用记录表"""

    __tablename__ = "skill_usage_records"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    session_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    skill_name: Mapped[str] = mapped_column(String(100), nullable=False)
    skill_category: Mapped[str] = mapped_column(String(50), nullable=False)
    before_intensity: Mapped[int] = mapped_column(Integer, nullable=False)
    after_intensity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    effectiveness: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    context: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )

    __table_args__ = (Index("idx_user_created_skill", "user_id", "created_at"),)


class CrisisEvent(Base):
    """危机事件表"""

    __tablename__ = "crisis_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    session_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    trigger_type: Mapped[str] = mapped_column(String(50), nullable=False)
    trigger_reason: Mapped[str] = mapped_column(Text, nullable=False)
    emotion_intensity: Mapped[int] = mapped_column(Integer, nullable=False)
    detected_keywords: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    risk_level: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    handled_by: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    handled_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    action_taken: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )

    __table_args__ = (Index("idx_user_status", "user_id", "status"),)


class EmotionImage(Base):
    """情绪图片表 (CAPS图库)"""

    __tablename__ = "emotion_images"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    image_id: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    category: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    valence: Mapped[float] = mapped_column(Float, nullable=False)
    valence_std: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    arousal: Mapped[float] = mapped_column(Float, nullable=False)
    arousal_std: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    dominance: Mapped[float] = mapped_column(Float, nullable=False)
    dominance_std: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )

    __table_args__ = (
        Index("idx_category_valence", "category", "valence"),
        Index("idx_vad", "valence", "arousal", "dominance"),
    )


class Admin(Base):
    """管理员表"""

    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), default="admin", nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
