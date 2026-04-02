"""
效果评估模块
评估DBT技能使用效果，计算情绪改善程度
"""
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class Evaluator:
    """效果评估器"""
    
    def __init__(self):
        """初始化评估器"""
        pass
    
    def evaluate_skill_effectiveness(
        self,
        before_intensity: int,
        after_intensity: int
    ) -> str:
        """
        评估技能使用效果
        :param before_intensity: 使用前情绪强度
        :param after_intensity: 使用后情绪强度
        :return: 效果等级
        """
        improvement = self.calculate_improvement(before_intensity, after_intensity)
        
        if improvement >= 3:
            return "very_effective"
        elif improvement >= 1:
            return "effective"
        elif improvement >= 0:
            return "slight"
        else:
            return "ineffective"
    
    def calculate_improvement(self, before: int, after: int) -> int:
        """
        计算改善值
        :param before: 使用前强度
        :param after: 使用后强度
        :return: 改善值（可为负）
        """
        return before - after
    
    def should_continue_recommendation(
        self,
        after_intensity: int,
        effectiveness: str
    ) -> bool:
        """
        判断是否需要继续推荐技能
        :param after_intensity: 使用后强度
        :param effectiveness: 效果等级
        :return: 是否继续
        """
        # 如果情绪强度已经很低，不需要继续
        if after_intensity <= 3:
            return False
        
        # 如果强度适中且效果良好，可以结束
        if after_intensity <= 6 and effectiveness in ["very_effective", "effective"]:
            return False
        
        # 其他情况继续推荐
        return True
    
    def save_skill_usage_record(self, usage_data: Dict, db_session=None) -> None:
        """
        保存使用记录到数据库
        :param usage_data: 使用数据
        :param db_session: 数据库会话
        """
        if not db_session:
            logger.warning("未提供数据库会话，无法保存技能使用记录")
            return
        
        try:
            from app.database.repositories.skill_repo import SkillUsageRepository
            repo = SkillUsageRepository(db_session)
            
            record_id = repo.save_skill_usage(usage_data)
            logger.info(f"保存技能使用记录: {record_id}")
            
        except Exception as e:
            logger.error(f"保存技能使用记录失败: {str(e)}")
    
    def generate_feedback_message(
        self,
        effectiveness: str,
        improvement: int
    ) -> str:
        """
        生成反馈消息
        :param effectiveness: 效果等级
        :param improvement: 改善值
        :return: 反馈消息
        """
        messages = {
            "very_effective": f"太好了！你的情绪强度降低了{improvement}分，这个技能对你很有效。",
            "effective": f"不错！你的情绪强度降低了{improvement}分，继续保持。",
            "slight": f"你的情绪有一点改善（降低{improvement}分），我们可以尝试其他技能。",
            "ineffective": "看起来这个技能效果不太明显，我们换一个试试吧。"
        }
        
        return messages.get(effectiveness, "感谢你的反馈。")
