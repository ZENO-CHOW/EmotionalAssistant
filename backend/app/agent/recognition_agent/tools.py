"""
识别AGENT工具模块
包含关键词匹配、紧急情况检测等工具函数
"""

from typing import Dict, List, Optional, Tuple, Any
import re


class CrisisDetector:
    """危机检测器"""

    CRISIS_KEYWORDS = {
        "suicide": [
            "自杀",
            "轻生",
            "不想活",
            "结束生命",
            "一了百了",
            "想死",
            "死了算了",
        ],
        "self_harm": ["自残", "伤害自己", "割腕", "自伤", "不想看到自己"],
        "hopeless": ["没有希望", "活不下去", "太痛苦了", "撑不住", "绝望", "没希望了"],
        "worthless": ["我很废物", "我没用", "我不配", "我是垃圾", "活着没意思"],
    }

    CRISIS_INTENSITY_THRESHOLD = 8

    def __init__(self, intensity_threshold: int = None):
        self.intensity_threshold = (
            intensity_threshold or self.CRISIS_INTENSITY_THRESHOLD
        )

    def detect_emergency(
        self, message: str, intensity: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        检测紧急情况

        Args:
            message: 用户消息
            intensity: 情绪强度（1-10）

        Returns:
            检测结果字典
        """
        result = {
            "detected": False,
            "type": None,
            "matched_keywords": [],
            "response": None,
            "risk_level": "low",
        }

        if not message:
            return result

        keyword_match = self._check_keywords(message)
        if keyword_match["detected"]:
            result["detected"] = True
            result["type"] = "keyword"
            result["matched_keywords"] = keyword_match["matched"]
            result["response"] = self._get_keyword_response(keyword_match["matched"])
            result["risk_level"] = "critical"
            return result

        if intensity is not None and intensity >= self.intensity_threshold:
            result["detected"] = True
            result["type"] = "high_intensity"
            result["response"] = self._get_high_intensity_response(intensity)
            result["risk_level"] = "high" if intensity >= 9 else "medium"
            return result

        return result

    def _check_keywords(self, message: str) -> Dict[str, Any]:
        """检查消息中的危机关键词"""
        matched = []
        message_lower = message.lower()

        for category, keywords in self.CRISIS_KEYWORDS.items():
            for keyword in keywords:
                if keyword in message:
                    matched.append({"category": category, "keyword": keyword})

        return {"detected": len(matched) > 0, "matched": matched}

    def _get_high_intensity_response(self, intensity: int) -> str:
        """生成高强度情绪响应"""
        return f"""我能感受到你现在情绪很强烈（{intensity}分），这种感觉一定很难受。

在我们尝试其他方法之前，先做一个快速的 TIPP 降阶技术，帮助身体快速降温：

1. **T（Temperature）**：用冷水洗洗脸，或者把冰块敷在脖子上
2. **I（Intense Exercise）**：原地快跑 30 秒
3. **P（Paced Breathing）**：深深吸气 4 秒，屏住 7 秒，慢慢呼气 8 秒
4. **P（Paired Muscle Relaxation）**：从脚开始，依次紧绷再放松全身肌肉

试完告诉我感觉如何。

如果你现在感到无法控制，请拨打：全国心理援助热线 400-161-9995"""

    def _get_keyword_response(self, matched_keywords: List[Dict]) -> str:
        """生成关键词触发的响应"""
        categories = [k["category"] for k in matched_keywords]

        if "suicide" in categories or "self_harm" in categories:
            return """听到你说这样的话，我很担心你。你不是一个人，我们一起想办法。

在你现在这种情况下，我建议你：
1. 告诉身边信任的人你的感受
2. 拨打心理援助热线：400-161-9995
3. 如果有自伤冲动，可以先做一些替代行为，比如用冰块握在手里

你现在方便告诉我，是什么让你有这样的想法吗？"""

        if "hopeless" in categories:
            return """听起来你现在感到非常绝望，好像没有出路。这种感觉是真实的，但我想告诉你，情况是可以改变的。

我建议你：
1. 现在方便和别人谈谈吗？朋友、家人、老师都可以
2. 把你的绝望感写下来，这有助于理清思绪
3. 拨打心理援助热线：400-161-9995

你不是一个人，我们一起想办法。"""

        return """听起来你现在正经历很大的困难，我理解你现在的感受。

如果你想找人谈谈，可以拨打：全国心理援助热线 400-161-9995

你现在方便告诉我更多关于你的感受吗？"""


def analyze_emotion_intensity(text: str) -> Optional[int]:
    """
    从文本中分析情绪强度

    Args:
        text: 用户输入文本

    Returns:
        估计的情绪强度（1-10），如果无法估计则返回None
    """
    text = text.lower()

    high_intensity_patterns = [
        r"非常.*(焦虑|痛苦|愤怒|恐惧|绝望)",
        r"极其|极度|特别.*(难过|痛苦|生气)",
        r"受不了|撑不住|要崩溃",
        r"太.*(难受|痛|生气|害怕)",
    ]

    for pattern in high_intensity_patterns:
        if re.search(pattern, text):
            return 8

    medium_intensity_patterns = [
        r"比较.*(焦虑|难过|生气|担心)",
        r"有些|相当.*(不安|紧张|伤心)",
        r"让我.*(烦恼|困扰|担心)",
    ]

    for pattern in medium_intensity_patterns:
        if re.search(pattern, text):
            return 5

    low_intensity_patterns = [r"有点|稍微|略微", r"一般|普通", r"还行|还好"]

    for pattern in low_intensity_patterns:
        if re.search(pattern, text):
            return 3

    return None
