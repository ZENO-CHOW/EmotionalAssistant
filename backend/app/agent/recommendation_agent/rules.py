"""
技能推荐规则
基于情绪类型和强度的推荐规则
"""

from typing import Dict, List, Optional


class SkillRecommendationRules:
    """技能推荐规则"""

    SKILL_RECOMMENDATION_RULES = {
        "anxiety": {
            "high": ["TIPP", "节律呼吸", "一心一意"],
            "medium": ["正念呼吸", "情绪命名", "接地技术"],
            "low": ["正念观察", "感恩练习"],
        },
        "anger": {
            "high": ["STOP", "剧烈运动", "冷水刺激"],
            "medium": ["慢慢呼吸", "情绪命名"],
            "low": ["自我安抚"],
        },
        "sadness": {
            "high": ["驾驭情绪之波", "自我安抚", "TIPP"],
            "medium": ["积极体验", "求助朋友"],
            "low": ["感恩练习"],
        },
        "fear": {
            "high": ["TIPP", "接地技术", "安全空间想象"],
            "medium": ["正念呼吸", "情绪命名"],
            "low": ["渐进式放松"],
        },
        "joy": {"all": ["正念享受", "感恩记录"]},
        "calm": {"all": ["价值澄清", "感恩练习"]},
    }

    EMOTION_CATEGORIES = {
        "anxiety": ["焦虑", "担心", "紧张", "不安", "害怕"],
        "anger": ["愤怒", "生气", "烦躁", "恼火"],
        "sadness": ["悲伤", "难过", "伤心", "失落"],
        "fear": ["恐惧", "害怕", "惊恐"],
        "joy": ["开心", "高兴", "快乐", "兴奋"],
        "calm": ["平静", "平静", "放松", "安心"],
    }

    INTENSITY_THRESHOLDS = {"high": 7, "medium": 4, "low": 0}

    @classmethod
    def get_recommended_skills(cls, emotion_type: str, intensity: int) -> List[str]:
        """
        根据情绪类型和强度获取推荐技能列表

        Args:
            emotion_type: 情绪类型
            intensity: 强度（1-10）

        Returns:
            推荐技能名称列表
        """
        emotion_rules = cls.SKILL_RECOMMENDATION_RULES.get(emotion_type)
        if not emotion_rules:
            return ["正念呼吸", "情绪命名"]

        intensity_level = cls._get_intensity_level(intensity)

        if "all" in emotion_rules:
            return emotion_rules["all"]

        return emotion_rules.get(intensity_level, emotion_rules.get("low", []))

    @classmethod
    def _get_intensity_level(cls, intensity: int) -> str:
        """根据强度值获取强度级别"""
        if intensity >= cls.INTENSITY_THRESHOLDS["high"]:
            return "high"
        elif intensity >= cls.INTENSITY_THRESHOLDS["medium"]:
            return "medium"
        return "low"

    @classmethod
    def get_skill_introduction(cls, skill_name: str) -> str:
        """获取技能简介"""
        from app.dbt.skills import SKILLS_DATABASE

        skill_data = SKILLS_DATABASE.get(skill_name)
        if skill_data:
            return skill_data.get("introduction", "")

        introductions = {
            "TIPP": "TIPP技能通过改变体温、剧烈运动、调整呼吸和放松肌肉来快速降低情绪强度",
            "正念呼吸": "通过专注于呼吸来稳定情绪，回到当下",
            "情绪命名": "准确识别和命名自己的情绪",
            "接地技术": "通过感官体验把注意力带回当下",
            "STOP": "STOP技能帮助你在冲动行为前暂停，避免做出后悔的决定",
            "自我安抚": "通过五感来安抚自己",
            "节律呼吸": "通过有节奏的深呼吸来调节自主神经系统",
            "一心一意": "全神贯注地做一件事",
            "感恩练习": "关注生活中值得感恩的事物",
            "正念观察": "以观察者身份不加评判地注意当下的体验",
            "正念享受": "全身心投入地体验积极事物",
            "感恩记录": "通过书写记录每天值得感恩的事情",
            "驾驭情绪之波": "像冲浪一样驾驭情绪的起伏",
            "安全空间想象": "在内心想象一个让你感到完全安全的地方",
            "渐进式放松": "通过逐步收紧和放松肌肉群来释放身体紧张",
            "剧烈运动": "通过高强度运动释放能量",
            "冷水刺激": "用冷水刺激面部，激活潜水反射",
            "慢慢呼吸": "通过放慢呼吸节奏来激活副交感神经系统",
            "积极体验": "主动创造积极的情绪体验",
            "求助朋友": "有效地向他人寻求帮助和支持",
        }

        return introductions.get(skill_name, "一个有用的情绪管理技能")

    @classmethod
    def get_skill_steps(cls, skill_name: str) -> List[Dict]:
        """获取技能的详细步骤"""
        from app.dbt.skills import SKILLS_DATABASE

        skill_data = SKILLS_DATABASE.get(skill_name)
        if skill_data:
            return skill_data.get("steps", [])

        return []
