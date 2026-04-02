"""
情绪日记相关数据模型
"""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum


class EmotionType(str, Enum):
    """情绪类型枚举"""

    JOY = "joy"
    CALM = "calm"
    SADNESS = "sadness"
    ANXIETY = "anxiety"
    ANGER = "anger"
    FEAR = "fear"


class BodyPartsSchema(BaseModel):
    """身体部位感受模型"""

    head: Optional[bool] = False
    chest: Optional[bool] = False
    stomach: Optional[bool] = False
    limbs: Optional[bool] = False


class CreateDiaryRequest(BaseModel):
    """创建日记请求模型"""

    emotion_type: Optional[EmotionType] = Field(None, description="情绪类型")
    emotion_label: Optional[str] = Field(
        None, min_length=1, max_length=50, description="情绪标签（中文）"
    )

    emotion: Optional[str] = Field(None, validation_alias="emotion_type")
    emotionLabel: Optional[str] = Field(None, validation_alias="emotion_label")

    emoji: str = Field(..., min_length=1, max_length=10, description="情绪表情符号")
    intensity: int = Field(..., ge=0, le=10, description="情绪强度(0-10)")
    content: Optional[str] = Field(None, max_length=1000, description="日记内容")
    triggers: Optional[List[str]] = Field(None, description="触发因素列表")
    body_parts: Optional[BodyPartsSchema] = Field(None, description="身体部位感受")
    selected_images: Optional[List[str]] = Field(
        None, description="选择的情绪图片ID列表"
    )
    diary_date: Optional[str] = Field(None, description="日记日期(YYYY-MM-DD)")

    @field_validator("diary_date")
    @classmethod
    def validate_diary_date(cls, v):
        """验证日记日期格式"""
        if v is not None:
            try:
                datetime.strptime(v, "%Y-%m-%d")
            except ValueError:
                raise ValueError("日期格式必须为YYYY-MM-DD")
        return v

    @model_validator(mode="before")
    @classmethod
    def normalize_emotion_fields(cls, data: Any) -> Any:
        """规范化情绪字段，兼容前端camelCase字段名"""
        if isinstance(data, dict):
            if data.get("emotion") is not None and data.get("emotion_type") is None:
                data["emotion_type"] = data["emotion"]
            if (
                data.get("emotionLabel") is not None
                and data.get("emotion_label") is None
            ):
                data["emotion_label"] = data["emotionLabel"]
        return data

    model_config = {"populate_by_name": True}


class UpdateDiaryRequest(BaseModel):
    """更新日记请求模型（所有字段可选）"""

    emotion_type: Optional[EmotionType] = None
    emotion_label: Optional[str] = Field(None, min_length=1, max_length=50)

    emotion: Optional[str] = Field(None, validation_alias="emotion_type")
    emotionLabel: Optional[str] = Field(None, validation_alias="emotion_label")

    emoji: Optional[str] = Field(None, min_length=1, max_length=10)
    intensity: Optional[int] = Field(None, ge=0, le=10)
    content: Optional[str] = Field(None, max_length=1000)
    triggers: Optional[List[str]] = None
    body_parts: Optional[BodyPartsSchema] = None
    selected_images: Optional[List[str]] = None

    @model_validator(mode="before")
    @classmethod
    def normalize_emotion_fields(cls, data: Any) -> Any:
        """规范化情绪字段，兼容前端camelCase字段名"""
        if isinstance(data, dict):
            if data.get("emotion") is not None and data.get("emotion_type") is None:
                data["emotion_type"] = data["emotion"]
            if (
                data.get("emotionLabel") is not None
                and data.get("emotion_label") is None
            ):
                data["emotion_label"] = data["emotionLabel"]
        return data

    model_config = {"populate_by_name": True}


class DiaryResponse(BaseModel):
    """日记响应模型"""

    id: str
    user_id: int
    emotion_type: str
    emotion_label: str
    emoji: str
    intensity: int
    content: Optional[str]
    triggers: Optional[List[str]]
    body_parts: Optional[Dict]
    selected_images: Optional[List[str]]
    created_at: datetime
    updated_at: datetime
    diary_date: str

    @property
    def emotion(self) -> str:
        """兼容前端字段名"""
        return self.emotion_type

    @property
    def emotionLabel(self) -> str:
        """兼容前端字段名"""
        return self.emotion_label

    def model_dump(self, *args, **kwargs) -> dict:
        """重写model_dump，添加兼容字段"""
        data = super().model_dump(*args, **kwargs)
        data["emotion"] = self.emotion_type
        data["emotionLabel"] = self.emotion_label
        return data

    model_config = {"from_attributes": True}


class DiaryListResponse(BaseModel):
    """日记列表响应模型"""

    list: List[DiaryResponse]
    total: int
    page: int
    page_size: int
    has_more: bool


class TrendPoint(BaseModel):
    """趋势数据点"""

    date: str
    average_intensity: Optional[float]
    record_count: int


class EmotionStatisticsResponse(BaseModel):
    """情绪统计响应模型"""

    total_records: int
    continuous_days: int
    emotion_distribution: Dict[str, int]
    average_intensity: float
    most_common_emotion: Optional[str]
    trend_data: List[TrendPoint]
