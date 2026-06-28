"""
对话模块相关数据模型
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    """消息角色枚举"""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class MessageType(str, Enum):
    """消息类型枚举"""

    TEXT = "text"
    IMAGE_SELECTION = "image_selection"
    INTENSITY_RATING = "intensity_rating"
    BODY_SELECTION = "body_selection"
    SKILL_CONFIRMATION = "skill_confirmation"
    STEP_COMPLETION = "step_completion"


class ChatMessageRequest(BaseModel):
    """发送消息请求模型"""

    message: str = Field(..., min_length=1, max_length=500, description="消息内容")
    session_id: Optional[str] = Field(None, description="会话ID(UUID)")
    message_type: MessageType = Field(MessageType.TEXT, description="消息类型")
    metadata: Optional[Dict] = Field(None, description="附加数据")


class RequiresInputSchema(BaseModel):
    """需要用户输入的组件信息"""

    type: str = Field(
        ...,
        description="""输入类型:
        - general/text: 普通文本输入
        - skill_confirmation: 技能确认
        - step_completion: 步骤完成确认
        - emotion_images: 情绪图片选择
        - intensity_slider: 强度滑块选择
        - body_selector: 身体部位选择
        - image_upload: 图片上传
    """,
    )
    prompt: str = Field(..., description="提示文本")
    options: Optional[List] = Field(None, description="选项列表")
    skill_name: Optional[str] = Field(None, description="技能名称")
    introduction: Optional[str] = Field(None, description="技能简介")
    step_number: Optional[int] = Field(None, description="当前步骤编号")
    total_steps: Optional[int] = Field(None, description="总步骤数")
    content: Optional[str] = Field(None, description="步骤内容")
    is_last_step: Optional[bool] = Field(None, description="是否最后一步")


class ChatMessageResponse(BaseModel):
    """消息响应模型"""

    reply: str = Field(..., description="AI回复内容")
    session_id: str = Field(..., description="会话ID")
    message_id: int = Field(..., description="消息ID")
    requires_input: Optional[RequiresInputSchema] = Field(
        None, description="需要用户输入的组件信息"
    )


class MessageItem(BaseModel):
    """消息项"""

    role: str
    content: str
    created_at: datetime
    metadata: Optional[Dict]

    model_config = {"from_attributes": True}


class EmotionChange(BaseModel):
    """情绪变化"""

    initial_intensity: Optional[int]
    final_intensity: Optional[int]
    improvement: Optional[int]


class ChatHistoryResponse(BaseModel):
    """会话历史响应模型"""

    session_id: str
    start_time: datetime
    end_time: Optional[datetime]
    status: str
    messages: List[MessageItem]
    summary: Optional[str]
    emotion_change: Optional[EmotionChange]

    model_config = {"from_attributes": True}


class SessionListItem(BaseModel):
    """会话列表项"""

    id: str
    start_time: datetime
    end_time: Optional[datetime]
    status: str
    summary: Optional[str]
    initial_emotion_type: Optional[str]

    model_config = {"from_attributes": True}


class SessionListResponse(BaseModel):
    """会话列表响应"""

    list: List[SessionListItem]
    total: int
    page: int
    page_size: int
