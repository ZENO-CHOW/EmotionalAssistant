"""
DBT技能推荐模块
根据情绪状态推荐DBT技能，个性化过滤低效技能
"""
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class SkillRecommender:
    """DBT技能推荐器"""
    
    # 推荐规则表（基于情绪类型和强度）
    SKILL_RULES = {
        "anxiety": {
            "high": ["TIPP", "节律呼吸", "一心一意"],  # 7-10分
            "medium": ["正念呼吸", "情绪命名", "接地技术"],  # 4-6分
            "low": ["正念观察", "感恩练习"]  # 1-3分
        },
        "anger": {
            "high": ["STOP", "剧烈运动", "冷水刺激"],
            "medium": ["痛苦耐受", "情绪调节", "慢慢呼吸"],
            "low": ["情绪命名", "自我安抚"]
        },
        "sadness": {
            "high": ["驾驭情绪之波", "自我安抚", "TIPP"],
            "medium": ["积极体验", "求助朋友", "情绪调节"],
            "low": ["感恩练习", "正念观察"]
        },
        "fear": {
            "high": ["TIPP", "接地技术", "安全空间想象"],
            "medium": ["正念呼吸", "情绪命名"],
            "low": ["渐进式放松", "正念观察"]
        },
        "joy": {
            "all": ["正念享受", "感恩记录", "分享快乐"]
        },
        "calm": {
            "all": ["价值澄清", "感恩练习", "正念冥想"]
        }
    }
    
    # 技能分类
    SKILL_CATEGORIES = {
        "TIPP": "distress_tolerance",
        "STOP": "distress_tolerance",
        "节律呼吸": "mindfulness",
        "一心一意": "mindfulness",
        "正念呼吸": "mindfulness",
        "情绪命名": "emotion_regulation",
        "接地技术": "distress_tolerance",
        "正念观察": "mindfulness",
        "感恩练习": "mindfulness",
        "剧烈运动": "distress_tolerance",
        "冷水刺激": "distress_tolerance",
        "痛苦耐受": "distress_tolerance",
        "情绪调节": "emotion_regulation",
        "慢慢呼吸": "mindfulness",
        "自我安抚": "emotion_regulation",
        "驾驭情绪之波": "emotion_regulation",
        "积极体验": "emotion_regulation",
        "求助朋友": "interpersonal",
        "安全空间想象": "mindfulness",
        "渐进式放松": "mindfulness",
        "正念享受": "mindfulness",
        "感恩记录": "mindfulness",
        "分享快乐": "interpersonal",
        "价值澄清": "mindfulness",
        "正念冥想": "mindfulness"
    }
    
    def __init__(self, db_session=None):
        """
        初始化推荐器
        :param db_session: 数据库会话（用于查询历史记录）
        """
        self.db = db_session
    
    def recommend_skill(
        self,
        emotion_type: str,
        intensity: int,
        user_id: Optional[int] = None,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        主推荐逻辑
        :param emotion_type: 情绪类型
        :param intensity: 情绪强度(0-10)
        :param user_id: 用户ID（用于个性化过滤）
        :param context: 上下文信息
        :return: 推荐结果
        """
        try:
            # 获取候选技能
            candidate_skills = self.get_suitable_skills(emotion_type, intensity)
            
            if not candidate_skills:
                logger.warning(f"未找到适合的技能: {emotion_type}, {intensity}")
                return {
                    "skill_name": None,
                    "reason": "暂时没有找到合适的技能",
                    "introduction": ""
                }
            
            # 个性化过滤（如果有用户ID和数据库）
            if user_id and self.db:
                candidate_skills = self.filter_ineffective_skills(user_id, candidate_skills)
            
            # 选择第一个技能
            if not candidate_skills:
                # 如果过滤后没有技能，使用默认技能
                candidate_skills = ["正念呼吸"]
            
            skill_name = candidate_skills[0]
            
            # 生成推荐理由
            reason = self._generate_reason(emotion_type, intensity, skill_name)
            
            # 获取技能简介
            from app.dbt.skills import get_skill_info
            skill_info = get_skill_info(skill_name)
            introduction = skill_info.get("introduction", "")
            
            result = {
                "skill_name": skill_name,
                "skill_category": self.SKILL_CATEGORIES.get(skill_name, "other"),
                "reason": reason,
                "introduction": introduction,
                "alternatives": candidate_skills[1:3] if len(candidate_skills) > 1 else []
            }
            
            logger.info(f"推荐技能: {skill_name} (情绪: {emotion_type}, 强度: {intensity})")
            return result
            
        except Exception as e:
            logger.error(f"技能推荐失败: {str(e)}")
            return {
                "skill_name": "正念呼吸",
                "reason": "系统推荐",
                "introduction": "通过专注呼吸来稳定情绪"
            }
    
    def get_suitable_skills(
        self,
        emotion_type: str,
        intensity: int
    ) -> List[str]:
        """
        从技能库筛选适用技能
        :param emotion_type: 情绪类型
        :param intensity: 情绪强度
        :return: 技能列表
        """
        # 确定强度等级
        if intensity >= 7:
            intensity_level = "high"
        elif intensity >= 4:
            intensity_level = "medium"
        else:
            intensity_level = "low"
        
        # 获取规则
        emotion_rules = self.SKILL_RULES.get(emotion_type, {})
        
        # 优先查找特定强度级别的技能
        skills = emotion_rules.get(intensity_level, [])
        
        # 如果没有，使用通用技能
        if not skills:
            skills = emotion_rules.get("all", [])
        
        # 如果还是没有，使用默认技能
        if not skills:
            skills = ["正念呼吸", "情绪命名"]
        
        return skills.copy()
    
    def filter_ineffective_skills(
        self,
        user_id: int,
        candidate_skills: List[str]
    ) -> List[str]:
        """
        查询用户历史使用记录，过滤低效技能
        :param user_id: 用户ID
        :param candidate_skills: 候选技能列表
        :return: 过滤后的技能列表
        """
        if not self.db:
            return candidate_skills
        
        try:
            from app.database.repositories.skill_repo import SkillUsageRepository
            repo = SkillUsageRepository(self.db)
            
            # 查询每个候选技能的历史记录
            filtered_skills = []
            for skill_name in candidate_skills:
                records = repo.get_user_skill_history(user_id, skill_name)
                
                # 如果没有历史记录，保留
                if not records:
                    filtered_skills.append(skill_name)
                    continue
                
                # 如果最近一次使用效果不是ineffective，保留
                latest_record = records[0]
                if latest_record.effectiveness != "ineffective":
                    filtered_skills.append(skill_name)
            
            # 如果过滤后为空，返回原列表
            return filtered_skills if filtered_skills else candidate_skills
            
        except Exception as e:
            logger.error(f"过滤技能失败: {str(e)}")
            return candidate_skills
    
    def _generate_reason(
        self,
        emotion_type: str,
        intensity: int,
        skill_name: str
    ) -> str:
        """
        生成推荐理由
        :param emotion_type: 情绪类型
        :param intensity: 情绪强度
        :param skill_name: 技能名称
        :return: 推荐理由
        """
        emotion_labels = {
            "anxiety": "焦虑",
            "anger": "愤怒",
            "sadness": "悲伤",
            "fear": "恐惧",
            "joy": "开心",
            "calm": "平静"
        }
        
        emotion_label = emotion_labels.get(emotion_type, "情绪")
        
        if intensity >= 7:
            intensity_desc = "比较强烈"
        elif intensity >= 4:
            intensity_desc = "中等程度"
        else:
            intensity_desc = "轻微"
        
        reason = f"根据你当前{intensity_desc}的{emotion_label}感受，{skill_name}可以帮助你快速调节情绪。"
        
        return reason
