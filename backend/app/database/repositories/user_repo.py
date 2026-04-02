"""
用户数据访问仓库
"""

from typing import Optional, List, Tuple
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from app.database.models import User


class UserRepository:
    """用户数据访问层"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username_or_email(self, identifier: str) -> Optional[User]:
        """根据用户名或邮箱获取用户"""
        return (
            self.db.query(User)
            .filter(or_(User.username == identifier, User.email == identifier))
            .first()
        )

    def create_user(
        self,
        username: str,
        password_hash: str,
        email: Optional[str] = None,
        nickname: Optional[str] = None,
        phone: Optional[str] = None,
        school: Optional[str] = None,
    ) -> User:
        """创建新用户"""
        user = User(
            username=username,
            nickname=nickname,
            email=email,
            password_hash=password_hash,
            phone=phone,
            school=school,
            status="active",
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_last_login(self, user_id: int) -> None:
        """更新用户最后登录时间"""
        self.db.query(User).filter(User.id == user_id).update(
            {"last_login_at": datetime.utcnow()}
        )
        self.db.commit()

    def update_user(self, user_id: int, updates: dict) -> bool:
        """更新用户信息"""
        result = self.db.query(User).filter(User.id == user_id).update(updates)
        self.db.commit()
        return result > 0

    def update_password(self, user_id: int, password_hash: str) -> bool:
        """更新用户密码"""
        return self.update_user(user_id, {"password_hash": password_hash})

    def change_user_status(self, user_id: int, status: str) -> bool:
        """更改用户状态"""
        return self.update_user(user_id, {"status": status})

    def list_users(
        self,
        status: Optional[str] = None,
        keyword: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Tuple[List[User], int]:
        """获取用户列表"""
        query = self.db.query(User)

        if status:
            query = query.filter(User.status == status)

        if keyword:
            query = query.filter(
                or_(
                    User.username.ilike(f"%{keyword}%"),
                    and_(User.email.isnot(None), User.email.ilike(f"%{keyword}%")),
                    User.phone.ilike(f"%{keyword}%"),
                    User.school.ilike(f"%{keyword}%"),
                )
            )

        total = query.count()
        users = query.offset((page - 1) * page_size).limit(page_size).all()

        return users, total

    def delete_user(self, user_id: int) -> bool:
        """删除用户"""
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False

    def check_username_exists(self, username: str) -> bool:
        """检查用户名是否已存在"""
        return self.db.query(User).filter(User.username == username).count() > 0

    def check_email_exists(self, email: str) -> bool:
        """检查邮箱是否已存在"""
        return self.db.query(User).filter(User.email == email).count() > 0

    def get_active_user_count(self) -> int:
        """获取活跃用户数量"""
        return self.db.query(User).filter(User.status == "active").count()

    def get_user_statistics(self) -> dict:
        """获取用户统计数据"""
        total = self.db.query(User).count()
        active = self.db.query(User).filter(User.status == "active").count()
        inactive = self.db.query(User).filter(User.status == "inactive").count()

        return {"total": total, "active": active, "inactive": inactive}

    def get_today_active_users(self) -> int:
        """获取今日活跃用户数量（基于last_login_at）"""
        today = date.today()
        today_start = datetime.combine(today, datetime.min.time())
        today_end = datetime.combine(today, datetime.max.time())

        return (
            self.db.query(User)
            .filter(User.last_login_at >= today_start, User.last_login_at <= today_end)
            .count()
        )

    def get_daily_active_users_count(
        self, start_date: date, end_date: date
    ) -> List[dict]:
        """
        获取每日活跃用户数量（基于last_login_at）
        :param start_date: 开始日期
        :param end_date: 结束日期
        :return: 每日活跃用户列表 [{date, count, label}, ...]
        """
        days_of_week = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

        query = (
            self.db.query(
                func.date(User.last_login_at).label("login_date"),
                func.count(func.distinct(User.id)).label("count"),
            )
            .filter(User.last_login_at >= start_date, User.last_login_at <= end_date)
            .group_by(func.date(User.last_login_at))
            .order_by(func.date(User.last_login_at))
            .all()
        )

        date_map = {date.fromisoformat(r.login_date): r.count for r in query}

        result = []
        current_date = start_date
        while current_date <= end_date:
            day_of_week = current_date.weekday()
            label = days_of_week[day_of_week]

            result.append(
                {
                    "date": current_date.isoformat(),
                    "count": date_map.get(current_date, 0),
                    "label": label,
                }
            )
            current_date += timedelta(days=1)

        return result

    def get_user_diary_count(self, user_id: int) -> int:
        """
        获取用户的情绪记录数量
        :param user_id: 用户ID
        :return: 日记数量
        """
        from app.database.models import EmotionDiary

        return (
            self.db.query(EmotionDiary).filter(EmotionDiary.user_id == user_id).count()
        )

    def get_user_risk_level(self, user_id: int) -> str:
        """
        获取用户风险等级（基于最近30天的情绪强度和危机事件）
        :param user_id: 用户ID
        :return: 风险等级 (high/medium/low)
        """
        from app.database.models import EmotionDiary, CrisisEvent
        from datetime import datetime, timedelta

        thirty_days_ago = datetime.utcnow() - timedelta(days=30)

        # 查询最近30天的情绪日记平均强度
        avg_intensity = (
            self.db.query(func.avg(EmotionDiary.intensity))
            .filter(
                EmotionDiary.user_id == user_id,
                EmotionDiary.created_at >= thirty_days_ago,
            )
            .scalar()
        )

        avg_intensity = float(avg_intensity) if avg_intensity else 0

        # 查询最近30天的危机事件
        crisis_events = (
            self.db.query(CrisisEvent)
            .filter(
                CrisisEvent.user_id == user_id,
                CrisisEvent.created_at >= thirty_days_ago,
            )
            .all()
        )

        # 判断是否有高危或中危危机事件
        has_high_risk_crisis = any(c.risk_level == "high" for c in crisis_events)
        has_medium_risk_crisis = any(c.risk_level == "medium" for c in crisis_events)

        # 计算风险等级
        if has_high_risk_crisis or (avg_intensity >= 8 and has_medium_risk_crisis):
            return "high"
        elif has_medium_risk_crisis or (6 <= avg_intensity < 8):
            return "medium"
        else:
            return "low"
