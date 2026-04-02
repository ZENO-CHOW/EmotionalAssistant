"""
危机检测模块
实时检测用户是否处于危机状态，多维度危机判定
"""
from typing import Dict, List, Tuple
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class CrisisDetector:
    """危机检测器"""
    
    # 危机关键词库
    CRISIS_KEYWORDS = {
        "suicide": ["自杀", "轻生", "不想活", "结束生命", "一了百了", "想死"],
        "self_harm": ["自残", "伤害自己", "割腕", "自伤"],
        "hopeless": ["没有希望", "活不下去", "太痛苦了", "撑不住", "绝望"],
        "worthless": ["我很废物", "我没用", "我不配", "我是垃圾"]
    }
    
    def __init__(self, db_session=None):
        """
        初始化检测器
        :param db_session: 数据库会话（用于查询历史记录）
        """
        self.db = db_session
        self.intensity_threshold = settings.CRISIS_INTENSITY_THRESHOLD
        self.keyword_enabled = settings.CRISIS_KEYWORD_ENABLED
        self.repeated_threshold = settings.CRISIS_REPEATED_THRESHOLD
        self.repeated_days = settings.CRISIS_REPEATED_DAYS
    
    def detect_crisis(
        self, 
        user_id: int, 
        message: str, 
        intensity: int, 
        session_id: str
    ) -> Dict:
        """
        执行危机检测
        :param user_id: 用户ID
        :param message: 用户消息
        :param intensity: 情绪强度
        :param session_id: 会话ID
        :return: 检测结果
        """
        try:
            is_crisis = False
            trigger_type = None
            trigger_reason = ""
            detected_keywords = []
            risk_level = "low"
            
            # 1. 强度阈值检测
            intensity_triggered, intensity_reason = self.check_intensity_threshold(intensity)
            if intensity_triggered:
                is_crisis = True
                trigger_type = "high_intensity"
                trigger_reason = intensity_reason
                risk_level = "high" if intensity >= 9 else "medium"
            
            # 2. 关键词检测
            if self.keyword_enabled:
                keyword_triggered, keywords = self.check_keyword_triggers(message)
                if keyword_triggered:
                    is_crisis = True
                    if not trigger_type:
                        trigger_type = "keywords"
                    trigger_reason += f" 检测到危机关键词: {', '.join(keywords)}"
                    detected_keywords = keywords
                    risk_level = "critical"  # 关键词触发视为最高风险
            
            # 3. 重复危机检测（需要数据库支持）
            if self.db and user_id:
                repeated_triggered = self.check_repeated_crisis(user_id)
                if repeated_triggered:
                    is_crisis = True
                    if not trigger_type:
                        trigger_type = "repeated_crisis"
                    trigger_reason += f" 近期多次高强度情绪"
                    if risk_level == "low":
                        risk_level = "medium"
            
            result = {
                "is_crisis": is_crisis,
                "risk_level": risk_level,
                "trigger_type": trigger_type,
                "trigger_reason": trigger_reason.strip(),
                "detected_keywords": detected_keywords,
                "user_id": user_id,
                "session_id": session_id,
                "emotion_intensity": intensity
            }
            
            if is_crisis:
                logger.warning(f"检测到危机事件: 用户{user_id}, 风险等级{risk_level}, 原因: {trigger_reason}")
            
            return result
            
        except Exception as e:
            logger.error(f"危机检测失败: {str(e)}")
            return {
                "is_crisis": False,
                "risk_level": "low",
                "trigger_type": None,
                "trigger_reason": "检测失败"
            }
    
    def check_intensity_threshold(self, intensity: int) -> Tuple[bool, str]:
        """
        强度阈值检测
        :param intensity: 情绪强度
        :return: (是否触发, 触发原因)
        """
        if intensity >= self.intensity_threshold:
            return True, f"情绪强度达到{intensity}分（阈值{self.intensity_threshold}分）"
        return False, ""
    
    def check_keyword_triggers(self, message: str) -> Tuple[bool, List[str]]:
        """
        关键词匹配检测
        :param message: 用户消息
        :return: (是否触发, 匹配的关键词列表)
        """
        matched_keywords = []
        
        for category, keywords in self.CRISIS_KEYWORDS.items():
            for keyword in keywords:
                if keyword in message:
                    matched_keywords.append(keyword)
        
        return len(matched_keywords) > 0, matched_keywords
    
    def check_repeated_crisis(self, user_id: int) -> bool:
        """
        查询数据库统计近期高强度记录
        :param user_id: 用户ID
        :return: 是否触发重复危机
        """
        if not self.db:
            return False
        
        try:
            from app.database.repositories.chat_repo import ChatRepository
            repo = ChatRepository(self.db)
            
            count = repo.get_recent_high_intensity_count(
                user_id=user_id,
                days=self.repeated_days,
                threshold=8  # 强度>8视为高强度
            )
            
            return count >= self.repeated_threshold
            
        except Exception as e:
            logger.error(f"查询历史记录失败: {str(e)}")
            return False
    
    def create_crisis_record(
        self, 
        crisis_data: Dict
    ) -> str:
        """
        创建危机事件记录
        :param crisis_data: 危机数据
        :return: crisis_event_id
        """
        if not self.db:
            logger.warning("未提供数据库会话，无法创建危机记录")
            return ""
        
        try:
            from app.database.repositories.crisis_repo import CrisisRepository
            repo = CrisisRepository(self.db)
            
            event_id = repo.create_crisis_event(crisis_data)
            logger.info(f"创建危机事件记录: {event_id}")
            
            return event_id
            
        except Exception as e:
            logger.error(f"创建危机记录失败: {str(e)}")
            return ""
    
    def get_crisis_response(self, risk_level: str) -> Dict:
        """
        生成危机干预话术
        :param risk_level: 风险等级
        :return: 干预话术和建议
        """
        # 共情话术
        empathy_messages = {
            "critical": "我听到你现在非常痛苦，这一定很难受。我想让你知道，你并不孤单。",
            "high": "听起来你现在正经历很大的困难，我理解你现在的感受。",
            "medium": "我能感受到你现在的压力和不安，这确实不容易。"
        }
        
        # 推荐技能
        recommended_skills = ["TIPP", "STOP"]
        
        # 专业求助热线
        hotlines = [
            "全国心理援助热线: 400-161-9995",
            "北京心理危机研究与干预中心: 010-82951332",
            "生命热线: 400-821-1215"
        ]
        
        # 组合回复
        response = {
            "empathy_message": empathy_messages.get(risk_level, empathy_messages["medium"]),
            "recommended_skills": recommended_skills,
            "hotlines": hotlines,
            "urgent_action": "如果你现在有伤害自己的想法，请立即拨打上述热线或前往最近的医院急诊。",
            "reassurance": "你的感受是真实的，寻求帮助是勇敢的表现。专业的心理咨询师可以提供更多支持。"
        }
        
        return response
