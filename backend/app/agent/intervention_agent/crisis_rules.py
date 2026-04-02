"""
危机干预规则和话术
包含紧急情况下的规则化响应模板
"""

from typing import Dict, List, Any, Optional


HIGH_INTENSITY_RESPONSE = {
    "empathy": "我能感受到你现在情绪很强烈，这种感觉一定很难受。",
    "immediate_suggestion": """在我们尝试其他方法之前，先做一个快速的 TIPP 降阶技术，帮助身体快速降温：

1. **T（Temperature）**：用冷水洗洗脸，或者把冰块敷在脖子上
2. **I（Intense Exercise）**：原地快跑 30 秒
3. **P（Paced Breathing）**：深深吸气 4 秒，屏住 7 秒，慢慢呼气 8 秒
4. **P（Paired Muscle Relaxation）**：从脚开始，依次紧绷再放松全身肌肉""",
    "follow_up": "试完告诉我感觉如何。如果你有更想尝试的方式，我也支持你。",
    "hotline": "如果你现在感到无法控制，请拨打：全国心理援助热线 400-161-9995",
}


KEYWORD_RESPONSE = {
    "suicide": {
        "empathy": "听到你说这样的话，我很担心你。你不是一个人，我们一起想办法。",
        "immediate_action": [
            "告诉身边信任的人你的感受",
            "拨打心理援助热线：400-161-9995",
            "如果有自伤冲动，可以先做一些替代行为，比如用冰块握在手里",
        ],
        "follow_up_question": "你现在方便告诉我，是什么让你有这样的想法吗？",
        "should_end": True,
    },
    "self_harm": {
        "empathy": "我能感受到你现在一定很痛苦。伤害自己可能是一种表达痛苦的方式，但我想帮助你找到其他方式。",
        "immediate_action": [
            "如果伤口需要处理，请先清理伤口",
            "找到可以替代自伤的方式：握冰块、画红线在手臂上",
            "告诉信任的人你的感受",
        ],
        "support_resource": "全国心理援助热线：400-161-9995",
        "should_end": True,
    },
    "hopeless": {
        "empathy": "听起来你现在感到非常绝望，好像没有出路。这种感觉是真实的，但我想告诉你，情况是可以改变的。",
        "immediate_action": [
            "你现在方便和别人谈谈吗？朋友、家人、老师都可以",
            "把你的绝望感写下来，这有助于理清思绪",
        ],
        "support_resource": "全国心理援助热线：400-161-9995",
        "should_end": True,
    },
    "worthless": {
        "empathy": "我能理解你会这样看待自己。在痛苦中，我们往往会对自己过于苛刻。",
        "immediate_action": [
            "试着想想，如果是你最好的朋友这样想，你会对他说什么？",
            "把这些自我批评的想法写下来，试着找出反证",
        ],
        "support_resource": "全国心理援助热线：400-161-9995",
        "should_end": False,
    },
}


def get_crisis_response(
    crisis_type: str,
    intensity: Optional[int] = None,
    matched_keywords: Optional[List[Dict]] = None,
) -> Dict[str, Any]:
    """
    获取危机响应

    Args:
        crisis_type: 危机类型 (high_intensity/keyword)
        intensity: 情绪强度
        matched_keywords: 匹配的关键词列表

    Returns:
        响应字典
    """
    if crisis_type == "high_intensity":
        return _get_high_intensity_response(intensity)
    elif crisis_type == "keyword":
        return _get_keyword_response(matched_keywords)
    else:
        return _get_default_response()


def _get_high_intensity_response(intensity: Optional[int] = None) -> Dict[str, Any]:
    """生成高强度情绪响应"""
    if intensity:
        empathy = f"我能感受到你现在情绪很强烈（{intensity}分），这种感觉一定很难受。"
    else:
        empathy = HIGH_INTENSITY_RESPONSE["empathy"]

    return {
        "response_type": "crisis",
        "empathy": empathy,
        "immediate_suggestion": HIGH_INTENSITY_RESPONSE["immediate_suggestion"],
        "follow_up": HIGH_INTENSITY_RESPONSE["follow_up"],
        "hotline": HIGH_INTENSITY_RESPONSE["hotline"],
        "should_end": False,
    }


def _get_keyword_response(
    matched_keywords: Optional[List[Dict]] = None,
) -> Dict[str, Any]:
    """生成关键词触发的响应"""
    if not matched_keywords:
        return _get_default_response()

    categories = [k["category"] for k in matched_keywords]

    for category in ["suicide", "self_harm", "hopeless", "worthless"]:
        if category in categories:
            keyword_response = KEYWORD_RESPONSE[category]
            return {
                "response_type": "crisis",
                "empathy": keyword_response["empathy"],
                "immediate_action": keyword_response.get("immediate_action", []),
                "follow_up_question": keyword_response.get("follow_up_question", ""),
                "support_resource": keyword_response.get("support_resource", ""),
                "should_end": keyword_response.get("should_end", False),
            }

    return _get_default_response()


def _get_default_response() -> Dict[str, Any]:
    """生成默认响应"""
    return {
        "response_type": "crisis",
        "empathy": "听起来你现在正经历很大的困难，我理解你现在的感受。",
        "immediate_action": [
            "告诉身边信任的人你的感受",
            "拨打心理援助热线：400-161-9995",
        ],
        "follow_up_question": "你现在方便告诉我更多关于你的感受吗？",
        "hotline": "全国心理援助热线 400-161-9995",
        "should_end": False,
    }


def format_crisis_response(response: Dict[str, Any]) -> str:
    """
    格式化危机响应为文本

    Args:
        response: 危机响应字典

    Returns:
        格式化的响应文本
    """
    parts = []

    if response.get("empathy"):
        parts.append(response["empathy"])

    if response.get("immediate_suggestion"):
        parts.append(response["immediate_suggestion"])
    elif response.get("immediate_action"):
        parts.append("我建议你：")
        for i, action in enumerate(response["immediate_action"], 1):
            parts.append(f"{i}. {action}")

    if response.get("follow_up") or response.get("follow_up_question"):
        parts.append("")
        if response.get("follow_up"):
            parts.append(response["follow_up"])
        if response.get("follow_up_question"):
            parts.append(response["follow_up_question"])

    if response.get("hotline") or response.get("support_resource"):
        parts.append("")
        hotline = response.get("hotline") or response.get("support_resource")
        parts.append(f"如果你需要更多帮助，请拨打：{hotline}")

    return "\n".join(parts)
