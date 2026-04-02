"""
LLM客户端封装
支持DeepSeek和OpenAI兼容的API
"""

import logging
from typing import List, Dict, Optional, Any
import json
from openai import OpenAI
from app.config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    """LLM客户端，封装DeepSeek API调用"""

    def __init__(self):
        """初始化LLM客户端"""
        if (
            not settings.LLM_API_KEY
            or settings.LLM_API_KEY == "your-deepseek-api-key-here"
        ):
            logger.warning("LLM API密钥未配置，将使用模拟模式")
            self.client = None
        else:
            self.client = OpenAI(
                api_key=settings.LLM_API_KEY, base_url=settings.LLM_BASE_URL
            )
            logger.info(
                f"LLM客户端初始化成功: {settings.LLM_BASE_URL}, 模型: {settings.LLM_MODEL}"
            )

    def _load_prompt(self, filename: str) -> str:
        """从文件加载提示词"""
        from pathlib import Path

        prompt_path = Path(__file__).parent.parent / "agent" / "prompts" / filename
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        system_prompt: Optional[str] = None,
    ) -> Optional[str]:
        """
        发送对话请求

        Args:
            messages: 消息列表，格式 [{"role": "user", "content": "..."}]
            temperature: 温度参数，控制随机性
            max_tokens: 最大token数
            system_prompt: 系统提示词

        Returns:
            AI回复内容，失败返回None
        """
        if not self.client:
            logger.warning("LLM未配置，返回None")
            return None

        try:
            # 构建完整消息
            full_messages = []
            if system_prompt:
                full_messages.append({"role": "system", "content": system_prompt})

            # 添加历史消息
            for msg in messages:
                if msg.get("role") and msg.get("content"):
                    full_messages.append(
                        {"role": msg["role"], "content": msg["content"]}
                    )

            # 调用API
            response = self.client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=full_messages,
                temperature=temperature or settings.LLM_TEMPERATURE,
                max_tokens=max_tokens or settings.LLM_MAX_TOKENS,
                timeout=settings.LLM_TIMEOUT,
            )

            # 提取回复
            reply = response.choices[0].message.content

            # 移除markdown格式符号（**）以避免在聊天界面显示
            if reply:
                reply = reply.replace("**", "")

            logger.info(f"LLM调用成功，回复长度: {len(reply)}")
            return reply

        except Exception as e:
            logger.error(f"LLM调用失败: {str(e)}")
            return None

    def analyze_emotion(
        self, user_message: str, conversation_history: List[Dict[str, str]] = None
    ) -> Optional[Dict]:
        """
        使用LLM分析文本情绪

        Args:
            user_message: 用户当前消息
            conversation_history: 对话历史（可选）

        Returns:
            情绪分析结果，格式: {
                "emotion_type": "anxiety",
                "intensity": 7,
                "confidence": 0.85,
                "reason": "用户提到..."
            }
        """
        if not self.client:
            return None

        system_prompt = """你是一个专业的情绪分析助手。请分析用户的情绪状态，并以JSON格式返回结果。

情绪类型包括：
- joy: 快乐、开心、兴奋
- calm: 平静、放松
- sadness: 悲伤、失落、沮丧
- anxiety: 焦虑、担心、紧张
- anger: 愤怒、生气、烦躁
- fear: 恐惧、害怕

强度范围：1-10（1最轻，10最重）
置信度：0.0-1.0

返回JSON格式：
{
    "emotion_type": "情绪类型",
    "intensity": 强度数字,
    "confidence": 置信度,
    "reason": "分析理由"
}"""

        try:
            full_messages = []

            if conversation_history:
                for msg in conversation_history:
                    if msg.get("role") and msg.get("content"):
                        full_messages.append(
                            {"role": msg["role"], "content": msg["content"]}
                        )

            full_messages.append({"role": "user", "content": user_message})

            logger.info(
                f"传递对话历史，共 {len(conversation_history) if conversation_history else 0} 条消息进行情绪分析"
            )

            response = self.chat(
                full_messages, system_prompt=system_prompt, temperature=0.3
            )

            if response:
                # 尝试解析JSON
                import json

                # 提取JSON部分（可能被markdown包裹）
                if "```json" in response:
                    response = response.split("```json")[1].split("```")[0].strip()
                elif "```" in response:
                    response = response.split("```")[1].split("```")[0].strip()

                result = json.loads(response)
                logger.info(f"情绪分析成功: {result}")
                return result

        except Exception as e:
            logger.error(f"情绪分析失败: {str(e)}")

        return None

    def recommend_skill(
        self, emotion_type: str, intensity: int, context: str = ""
    ) -> Optional[Dict]:
        """
        使用LLM推荐DBT技能

        Args:
            emotion_type: 情绪类型
            intensity: 强度(1-10)
            context: 上下文信息

        Returns:
            推荐结果，格式: {
                "skill_name": "TIPP",
                "reason": "推荐理由",
                "introduction": "技能简介"
            }
        """
        if not self.client:
            return None

        from ..dbt.skills import SKILLS_DATABASE

        # 构建可用技能列表
        skills_info = []
        for skill_name, skill_data in SKILLS_DATABASE.items():
            skills_info.append(f"- {skill_name}: {skill_data.get('introduction', '')}")

        system_prompt = f"""你是一个专业的DBT（辩证行为疗法）技能推荐助手。

可用的DBT技能：
{chr(10).join(skills_info)}

请根据用户的情绪状态推荐最合适的技能，并以JSON格式返回：
{{
    "skill_name": "技能名称（必须从上述列表中选择）",
    "reason": "推荐理由（一句话说明为什么推荐这个技能）",
    "introduction": "用温暖的话术介绍这个技能（让用户愿意尝试）"
}}"""

        user_message = f"用户当前情绪：{emotion_type}，强度：{intensity}/10"
        if context:
            user_message += f"\n背景：{context}"

        try:
            messages = [{"role": "user", "content": user_message}]
            response = self.chat(messages, system_prompt=system_prompt, temperature=0.5)

            if response:
                import json

                if "```json" in response:
                    response = response.split("```json")[1].split("```")[0].strip()
                elif "```" in response:
                    response = response.split("```")[1].split("```")[0].strip()

                result = json.loads(response)
                logger.info(f"技能推荐成功: {result}")
                return result

        except Exception as e:
            logger.error(f"技能推荐失败: {str(e)}")

        return None

    def generate_guidance(
        self,
        skill_name: str,
        skill_category: str,
        total_steps: int,
        current_step: int,
        step_content: str,
        user_context: str = "",
    ) -> str:
        """生成技能引导话术"""
        if not self.client:
            return "请按照以下步骤进行练习..."

        try:
            system_prompt = self._load_prompt("skill_guidance_prompt.txt")
        except:
            system_prompt = "你是一个专业的情绪管理助手，请引导用户完成技能练习。"

        user_message = f"""当前技能：{skill_name}
技能分类：{skill_category}
技能步骤（共{total_steps}步）：请按步骤引导
当前步骤：第{current_step}步
步骤内容：{step_content}
用户场景：{user_context}"""

        messages = [{"role": "user", "content": user_message}]
        response = self.chat(messages, system_prompt=system_prompt)
        return response or "请继续下一步练习。"

    def generate_response(
        self, system_prompt: str, user_message: str, context: Dict[str, Any] = None
    ) -> str:
        """通用对话生成"""
        if context:
            context_str = "\n".join([f"- {k}: {v}" for k, v in context.items()])
            system_prompt += f"\n\n当前状态信息：\n{context_str}"

        messages = [{"role": "user", "content": user_message}]
        response = self.chat(messages, system_prompt=system_prompt)
        return response or "我理解你的感受。"

    def stream_chat(self, messages: List[Dict[str, str]]):
        """流式对话（用于最终响应）"""
        if not self.client:
            yield "LLM未配置"
            return

        try:
            response = self.client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=messages,
                temperature=settings.LLM_TEMPERATURE,
                stream=True,
            )

            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            logger.error(f"流式对话失败: {str(e)}")
            yield "对话失败，请稍后重试。"

    def _parse_json_response(self, response) -> Dict:
        """解析 JSON 响应"""
        content = response.choices[0].message.content
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            logger.error(f"JSON 解析失败: {content}")
            return {"error": "解析失败", "raw": content}


# 全局单例
_llm_client = None


def get_llm_client() -> LLMClient:
    """获取LLM客户端单例"""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client
