"""
情绪识别模块
分析用户文字消息提取情绪信号，支持多模态输入
"""

from typing import Dict, List, Optional, Tuple
import json
import logging
import re

logger = logging.getLogger(__name__)


class EmotionRecognizer:
    """情绪识别器"""

    # 情绪关键词库
    EMOTION_KEYWORDS = {
        "joy": ["开心", "高兴", "快乐", "喜悦", "兴奋", "愉快", "欣喜", "满足"],
        "calm": ["平静", "放松", "舒适", "安宁", "淡定", "平和", "宁静"],
        "sadness": ["难过", "伤心", "悲伤", "失落", "沮丧", "郁闷", "低落", "痛苦"],
        "anxiety": ["焦虑", "紧张", "担心", "不安", "忐忑", "害怕", "恐慌", "压力"],
        "anger": ["生气", "愤怒", "恼火", "烦躁", "气愤", "愤恨", "暴躁"],
        "fear": ["恐惧", "害怕", "惊恐", "畏惧", "胆怯", "恐慌"],
    }

    # 强度关键词
    INTENSITY_KEYWORDS = {
        "high": ["非常", "特别", "极其", "太", "超级", "十分", "很", "极度"],
        "medium": ["有点", "稍微", "比较", "还算", "略微"],
        "low": ["一点", "轻微", "微微"],
    }

    def __init__(self):
        """初始化识别器"""
        from .llm_client import get_llm_client

        self.llm_client = get_llm_client()

    def analyze_text_emotion(
        self, text: str, conversation_history: Optional[List[Dict]] = None
    ) -> Dict:
        """
        分析文字情绪
        :param text: 用户输入文字
        :param conversation_history: 对话历史（可用于上下文理解）
        :return: 情绪分析结果
        """
        try:
            # 优先使用LLM分析
            llm_result = self.llm_client.analyze_emotion(text)

            if llm_result:
                # LLM分析成功
                result = {
                    "emotion_type": llm_result.get("emotion_type"),
                    "intensity": llm_result.get("intensity", 5),
                    "confidence": llm_result.get("confidence", 0.8),
                    "need_more_info": llm_result.get("confidence", 0.8) < 0.6,
                    "reason": f"AI分析：{llm_result.get('reason', '')}",
                }
                logger.info(f"文字情绪分析结果（LLM）: {result}")
                return result

            # LLM不可用，回退到关键词匹配
            logger.warning("LLM不可用，使用关键词匹配")

            # 关键词匹配识别情绪类型
            emotion_scores = self._keyword_matching(text)

            # 识别强度
            intensity = self._analyze_intensity(text)

            # 获取最高分的情绪
            if emotion_scores:
                emotion_type = max(emotion_scores.items(), key=lambda x: x[1])[0]
                confidence = min(
                    emotion_scores[emotion_type] / 3.0, 1.0
                )  # 归一化置信度
                need_more_info = confidence < 0.5
            else:
                emotion_type = None
                confidence = 0.0
                need_more_info = True

            result = {
                "emotion_type": emotion_type,
                "intensity": intensity,
                "confidence": round(confidence, 2),
                "need_more_info": need_more_info,
                "reason": f"基于关键词匹配识别：{emotion_scores}"
                if emotion_scores
                else "未识别到明确情绪关键词",
            }

            logger.info(f"文字情绪分析结果（关键词）: {result}")
            return result

        except Exception as e:
            logger.error(f"文字情绪分析失败: {str(e)}")
            return {
                "emotion_type": None,
                "intensity": 5,
                "confidence": 0.0,
                "need_more_info": True,
                "reason": "分析失败",
            }

    def _keyword_matching(self, text: str) -> Dict[str, int]:
        """
        关键词匹配
        :param text: 文字内容
        :return: 各情绪类型的匹配得分
        """
        scores = {}
        for emotion_type, keywords in self.EMOTION_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                scores[emotion_type] = score
        return scores

    def _analyze_intensity(self, text: str) -> int:
        """
        分析情绪强度
        :param text: 文字内容
        :return: 强度值(0-10)
        """
        # 检查强度关键词
        for level, keywords in self.INTENSITY_KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                if level == "high":
                    return 8
                elif level == "medium":
                    return 5
                elif level == "low":
                    return 3

        # 检查感叹号数量（表示情绪强烈程度）
        exclamation_count = text.count("！") + text.count("!")
        if exclamation_count >= 3:
            return 9
        elif exclamation_count >= 2:
            return 7
        elif exclamation_count >= 1:
            return 6

        # 默认中等强度
        return 5

    def process_image_selection(self, image_ids: List[str]) -> Dict:
        """
        处理情绪图片选择
        基于IAPS/GAPED标准化图片库的效价和唤醒度

        :param image_ids: 选择的图片ID列表
        :return: 情绪分析结果
        """
        try:
            # 简化版本：模拟图片情绪映射
            # 实际应从数据库查询图片的valence和arousal属性

            # 模拟图片ID到情绪的映射
            image_emotion_map = {
                "img_anxiety_": "anxiety",
                "img_sadness_": "sadness",
                "img_anger_": "anger",
                "img_joy_": "joy",
                "img_calm_": "calm",
                "img_fear_": "fear",
            }

            # 统计选择的图片对应的情绪
            emotion_counts: Dict[str, int] = {}
            for img_id in image_ids:
                for prefix, emotion in image_emotion_map.items():
                    if img_id.startswith(prefix):
                        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

            if emotion_counts:
                emotion_type = max(emotion_counts.items(), key=lambda x: x[1])[0]
                confidence = min(len(image_ids) / 3.0, 1.0)
            else:
                emotion_type = None
                confidence = 0.0

            result = {
                "emotion_type": emotion_type,
                "confidence": round(confidence, 2),
                "source": "image_selection",
            }

            logger.info(f"图片选择情绪分析: {result}")
            return result

        except Exception as e:
            logger.error(f"图片情绪分析失败: {str(e)}")
            return {"emotion_type": None, "confidence": 0.0}

    def combine_multimodal_inputs(
        self,
        text_result: Optional[Dict] = None,
        image_result: Optional[Dict] = None,
        intensity_rating: Optional[int] = None,
    ) -> Dict:
        """
        综合多模态输入
        :param text_result: 文字分析结果
        :param image_result: 图片分析结果
        :param intensity_rating: 用户评分
        :return: 综合情绪判断
        """
        try:
            # 收集所有有效的情绪类型
            emotion_votes = []
            confidences = []

            if text_result and text_result.get("emotion_type"):
                emotion_votes.append(text_result["emotion_type"])
                confidences.append(text_result.get("confidence", 0.5))

            if image_result and image_result.get("emotion_type"):
                emotion_votes.append(image_result["emotion_type"])
                confidences.append(image_result.get("confidence", 0.5))

            # 投票决定最终情绪
            if emotion_votes:
                # 简单多数投票
                from collections import Counter

                vote_counts = Counter(emotion_votes)
                emotion_type = vote_counts.most_common(1)[0][0]

                # 综合置信度
                avg_confidence = sum(confidences) / len(confidences)
                final_confidence = min(avg_confidence * 1.2, 1.0)  # 多模态提升置信度
            else:
                emotion_type = None
                final_confidence = 0.0

            # 确定强度
            if intensity_rating is not None:
                intensity = intensity_rating
            elif text_result and text_result.get("intensity"):
                intensity = text_result["intensity"]
            else:
                intensity = 5

            result = {
                "emotion_type": emotion_type,
                "intensity": intensity,
                "confidence": round(final_confidence, 2),
                "sources": [],
            }

            if text_result and text_result.get("emotion_type"):
                result["sources"].append("text")
            if image_result and image_result.get("emotion_type"):
                result["sources"].append("image")
            if intensity_rating is not None:
                result["sources"].append("rating")

            logger.info(f"多模态综合结果: {result}")
            return result

        except Exception as e:
            logger.error(f"多模态综合失败: {str(e)}")
            return {"emotion_type": None, "intensity": 5, "confidence": 0.0}
