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
from sqlalchemy.sql import func
from datetime import datetime
from app.database.connection import Base


class User(Base):
    """用户表"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    nickname = Column(String(50), nullable=True)  # 昵称，可独立于用户名修改
    email = Column(String(100), unique=True, nullable=True, index=True)
    password_hash = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    school = Column(String(100), nullable=True)
    avatar = Column(String(255), nullable=True)
    status = Column(String(20), default="active", nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    last_login_at = Column(DateTime, nullable=True)


class ChatSession(Base):
    """对话会话表"""

    __tablename__ = "chat_sessions"

    id = Column(String(36), primary_key=True, index=True)  # UUID
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    start_time = Column(DateTime, default=func.now(), nullable=False)
    end_time = Column(DateTime, nullable=True)
    status = Column(String(20), default="active", nullable=False)
    summary = Column(Text, nullable=True)
    initial_emotion_type = Column(String(50), nullable=True)
    initial_intensity = Column(Integer, nullable=True)
    final_intensity = Column(Integer, nullable=True)
    recommended_skills = Column(Text, nullable=True)  # JSON array
    is_crisis = Column(Boolean, default=False, nullable=False)
    assessment_status = Column(
        String(20), default="not_started", nullable=False
    )  # not_started/in_progress/completed
    assessment_data = Column(
        Text, nullable=True
    )  # JSON: {message_count, step, selected_image, body_parts, intensity}
    agent_state = Column(Text, nullable=True)  # JSON: 多AGENT完整状态

    __table_args__ = (Index("idx_user_start_time", "user_id", "start_time"),)


class ChatMessage(Base):
    """对话消息表"""

    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    session_id = Column(
        String(36),
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role = Column(String(20), nullable=False)  # user/assistant/system
    content = Column(Text, nullable=False)
    message_type = Column(String(30), default="text", nullable=False)
    extra_data = Column(Text, nullable=True)  # JSON
    created_at = Column(DateTime, default=func.now(), nullable=False)

    __table_args__ = (Index("idx_session_created", "session_id", "created_at"),)


class EmotionDiary(Base):
    """情绪日记表"""

    __tablename__ = "emotion_diaries"

    id = Column(String(36), primary_key=True, index=True)  # UUID
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    emotion_type = Column(String(50), nullable=False)
    emotion_label = Column(String(50), nullable=False)
    emoji = Column(String(10), nullable=False)
    intensity = Column(Integer, nullable=False)
    content = Column(Text, nullable=True)
    triggers = Column(Text, nullable=True)  # JSON array
    body_parts = Column(Text, nullable=True)  # JSON object
    selected_images = Column(Text, nullable=True)  # JSON array
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
    diary_date = Column(Date, nullable=False, index=True)

    __table_args__ = (
        Index("idx_user_diary_date", "user_id", "diary_date", unique=True),
        Index("idx_user_created", "user_id", "created_at"),
    )


class SkillUsageRecord(Base):
    """DBT技能使用记录表"""

    __tablename__ = "skill_usage_records"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    session_id = Column(
        String(36),
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    skill_name = Column(String(100), nullable=False)
    skill_category = Column(String(50), nullable=False)
    before_intensity = Column(Integer, nullable=False)
    after_intensity = Column(Integer, nullable=True)
    effectiveness = Column(String(20), nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    context = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    __table_args__ = (Index("idx_user_created_skill", "user_id", "created_at"),)


class CrisisEvent(Base):
    """危机事件表"""

    __tablename__ = "crisis_events"

    id = Column(String(36), primary_key=True, index=True)  # UUID
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    session_id = Column(
        String(36),
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    trigger_type = Column(String(50), nullable=False)
    trigger_reason = Column(Text, nullable=False)
    emotion_intensity = Column(Integer, nullable=False)
    detected_keywords = Column(Text, nullable=True)  # JSON array
    risk_level = Column(String(20), nullable=False)
    status = Column(String(20), default="pending", nullable=False)
    handled_by = Column(Integer, nullable=True)
    handled_at = Column(DateTime, nullable=True)
    action_taken = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    __table_args__ = (Index("idx_user_status", "user_id", "status"),)


class EmotionImage(Base):
    """情绪图片表 (CAPS图库)"""

    __tablename__ = "emotion_images"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    image_id = Column(
        String(50), unique=True, nullable=False, index=True
    )  # 如: "1001", "_3292", "2100"
    name = Column(String(100), nullable=True)  # 图片名称/描述
    category = Column(
        String(20), nullable=False, index=True
    )  # positive/negative/neutral
    valence = Column(Float, nullable=False)  # 效价 (1-9)
    valence_std = Column(Float, nullable=True)  # 效价标准差
    arousal = Column(Float, nullable=False)  # 唤醒度 (1-9)
    arousal_std = Column(Float, nullable=True)  # 唤醒度标准差
    dominance = Column(Float, nullable=False)  # 支配度 (1-9)
    dominance_std = Column(Float, nullable=True)  # 支配度标准差
    file_path = Column(
        String(255), nullable=False
    )  # 相对路径: /static/images/caps/positive/1001.jpg
    created_at = Column(DateTime, default=func.now(), nullable=False)

    __table_args__ = (
        Index("idx_category_valence", "category", "valence"),
        Index("idx_vad", "valence", "arousal", "dominance"),
    )


class Admin(Base):
    """管理员表"""

    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="admin", nullable=False)  # super_admin, admin
    status = Column(String(20), default="active", nullable=False)  # active, inactive
    last_login_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
