"""
DBT技能使用记录数据访问层
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database.models import SkillUsageRecord


class SkillUsageRepository:
    """技能使用记录Repository"""

    def __init__(self, db: Session):
        self.db = db

    def save_skill_usage(self, usage_data: dict) -> int:
        """保存技能使用记录"""
        record = SkillUsageRecord(**usage_data)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return int(record.id)  # type: ignore

    def get_user_skill_history(
        self, user_id: int, skill_name: Optional[str] = None
    ) -> List[SkillUsageRecord]:
        """获取用户技能历史使用记录"""
        query = self.db.query(SkillUsageRecord).filter(
            SkillUsageRecord.user_id == user_id
        )

        if skill_name:
            query = query.filter(SkillUsageRecord.skill_name == skill_name)

        return query.order_by(SkillUsageRecord.created_at.desc()).all()

    def get_effective_skills(self, user_id: int) -> List[str]:
        """获取用户使用有效的技能列表"""
        records = (
            self.db.query(SkillUsageRecord.skill_name)
            .filter(
                SkillUsageRecord.user_id == user_id,
                SkillUsageRecord.effectiveness.in_(["very_effective", "effective"]),
            )
            .distinct()
            .all()
        )

        return [r[0] for r in records]
