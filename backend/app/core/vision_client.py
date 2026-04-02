"""
视觉识别客户端
使用 OpenAI 兼容 API 调用 Qwen/Qwen3-VL-30B-A3B-Instruct
"""

import base64
import logging
from typing import Optional, Dict
from openai import OpenAI
from app.config import settings

logger = logging.getLogger(__name__)


class VisionClient:
    """图片情绪识别客户端"""

    def __init__(self):
        if not settings.VISION_API_KEY:
            logger.warning("VISION_API_KEY 未配置，VisionClient 将使用模拟模式")
            self.client = None
        else:
            self.client = OpenAI(
                api_key=settings.VISION_API_KEY, base_url=settings.VISION_BASE_URL
            )
        self.model = settings.VISION_MODEL or "Qwen/Qwen3-VL-30B-A3B-Instruct"

    def recognize_emotion(self, image_url: str) -> Optional[Dict]:
        """
        分析图片中的情绪

        Args:
            image_url: 图片 URL

        Returns:
            {
                "emotion_type": "anxiety",
                "confidence": 0.85,
                "reason": "图片显示皱眉、嘴角下垂..."
            }
        """
        if not self.client:
            return self._mock_response()

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """你是一个专业的情绪分析助手。请分析这张图片中人物的情绪状态。

请从以下情绪类型中选择：
- joy: 快乐、开心、兴奋
- calm: 平静、放松
- sadness: 悲伤、失落、沮丧
- anxiety: 焦虑、担心、紧张
- anger: 愤怒、生气、烦躁
- fear: 恐惧、害怕

请以 JSON 格式返回分析结果：
{
    "emotion_type": "情绪类型",
    "confidence": 置信度(0-1),
    "reason": "分析理由（50字内）"
}""",
                            },
                            {"type": "image_url", "image_url": {"url": image_url}},
                        ],
                    }
                ],
                temperature=0.3,
                max_tokens=500,
            )

            response_content = response.choices[0].message.content
            if response_content is None:
                logger.warning("图片识别响应内容为空")
                return self._mock_response()
            return self._parse_response(response_content)

        except Exception as e:
            logger.error(f"图片情绪识别失败: {str(e)}")
            return self._mock_response()

    def _parse_response(self, response: str) -> Dict:
        """解析 LLM 返回的 JSON 结果"""
        import json

        try:
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()

            result = json.loads(response)
            logger.info(f"图片情绪识别成功: {result}")
            return result

        except (json.JSONDecodeError, IndexError) as e:
            logger.error(f"解析图片识别结果失败: {e}")
            return {
                "emotion_type": "calm",
                "confidence": 0.5,
                "reason": "无法准确识别，使用默认值",
            }

    def _mock_response(self) -> Dict:
        """模拟响应（API 未配置时使用）"""
        return {
            "emotion_type": "calm",
            "confidence": 0.5,
            "reason": "API 未配置，使用模拟结果",
        }


_vision_client = None


def get_vision_client() -> VisionClient:
    """获取视觉客户端单例"""
    global _vision_client
    if _vision_client is None:
        _vision_client = VisionClient()
    return _vision_client
