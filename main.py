from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# 初始化FastAPI应用，定义API标题
app = FastAPI(title="Emotional Management Assistant API")


# 定义用户情绪输入数据模型，用于接收前端发送的情绪分析请求
class UserEmotionInput(BaseModel):
    user_id: str  # 用户唯一标识符
    emotion_text: str  # 用户输入的情绪描述文本
    timestamp: Optional[str] = None  # 可选的时间戳字段


# 定义情绪响应数据模型，用于返回情绪分析结果
class EmotionResponse(BaseModel):
    emotion: str  # 识别出的情绪类型
    intensity: float  # 情绪强度（0-1之间）
    suggested_skill: str  # 建议使用的DBT技能


# 根路径端点，用于验证API是否正常运行
@app.get("/")
async def root():
    return {"message": "Emotional Management Assistant API"}


# 情绪分析端点：接收用户输入的文本，分析情绪并返回建议的DBT技能
@app.post("/api/analyze-emotion", response_model=EmotionResponse)
async def analyze_emotion(input_data: UserEmotionInput):
    return EmotionResponse(
        emotion="anxious", intensity=0.75, suggested_skill="TIPP技巧"
    )


# 技能查询端点：根据技能名称返回对应的DBT技能描述
@app.get("/api/skills/{skill_name}")
async def get_skill(skill_name: str):
    skills = {
        "tipp": "Temperature, Intense exercise, Paced breathing, Paired muscle relaxation",
        "stop": "Stop, Take a step back, Observe, Proceed mindfully",
        "mindfulness": "Be present in the moment without judgment",
    }
    return {
        "skill": skill_name,
        "description": skills.get(skill_name, "Skill not found"),
    }
