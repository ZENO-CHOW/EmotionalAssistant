"""
管理员数据访问仓库
"""

from typing import Optional, List, Tuple
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database.models import Admin


class AdminRepository:
    """管理员数据访问层"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, admin_id: int) -> Optional[Admin]:
        """根据ID获取管理员"""
        return self.db.query(Admin).filter(Admin.id == admin_id).first()

    def get_by_username(self, username: str) -> Optional[Admin]:
        """根据用户名获取管理员"""
        return self.db.query(Admin).filter(Admin.username == username).first()

    def get_by_email(self, email: str) -> Optional[Admin]:
        """根据邮箱获取管理员"""
        return self.db.query(Admin).filter(Admin.email == email).first()

    def get_by_username_or_email(self, identifier: str) -> Optional[Admin]:
        """根据用户名或邮箱获取管理员"""
        return (
            self.db.query(Admin)
            .filter(or_(Admin.username == identifier, Admin.email == identifier))
            .first()
        )

    def create_admin(
        self, username: str, email: str, password_hash: str, role: str = "admin"
    ) -> Admin:
        """创建新管理员"""
        admin = Admin(
            username=username,
            email=email,
            password_hash=password_hash,
            role=role,
            status="active",
        )
        self.db.add(admin)
        self.db.commit()
        self.db.refresh(admin)
        return admin

    def update_last_login(self, admin_id: int) -> None:
        """更新管理员最后登录时间"""
        self.db.query(Admin).filter(Admin.id == admin_id).update(
            {"last_login_at": datetime.utcnow()}
        )
        self.db.commit()

    def update_admin(self, admin_id: int, updates: dict) -> bool:
        """更新管理员信息"""
        result = self.db.query(Admin).filter(Admin.id == admin_id).update(updates)
        self.db.commit()
        return result > 0

    def update_password(self, admin_id: int, password_hash: str) -> bool:
        """更新管理员密码"""
        return self.update_admin(admin_id, {"password_hash": password_hash})

    def change_admin_status(self, admin_id: int, status: str) -> bool:
        """更改管理员状态"""
        return self.update_admin(admin_id, {"status": status})

    def list_admins(
        self,
        role: Optional[str] = None,
        status: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Tuple[List[Admin], int]:
        """获取管理员列表"""
        query = self.db.query(Admin)

        if role:
            query = query.filter(Admin.role == role)

        if status:
            query = query.filter(Admin.status == status)

        total = query.count()
        admins = query.offset((page - 1) * page_size).limit(page_size).all()

        return admins, total

    def delete_admin(self, admin_id: int) -> bool:
        """删除管理员"""
        admin = self.get_by_id(admin_id)
        if admin:
            self.db.delete(admin)
            self.db.commit()
            return True
        return False

    def check_username_exists(self, username: str) -> bool:
        """检查用户名是否已存在"""
        return self.db.query(Admin).filter(Admin.username == username).count() > 0

    def check_email_exists(self, email: str) -> bool:
        """检查邮箱是否已存在"""
        return self.db.query(Admin).filter(Admin.email == email).count() > 0

    def get_active_admin_count(self) -> int:
        """获取活跃管理员数量"""
        return self.db.query(Admin).filter(Admin.status == "active").count()

    def get_admin_statistics(self) -> dict:
        """获取管理员统计数据"""
        total = self.db.query(Admin).count()
        active = self.db.query(Admin).filter(Admin.status == "active").count()
        super_admin = self.db.query(Admin).filter(Admin.role == "super_admin").count()

        return {"total": total, "active": active, "super_admin": super_admin}
