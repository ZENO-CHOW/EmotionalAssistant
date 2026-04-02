"""
数据库初始化脚本
创建默认用户和管理员账户
"""

import sys
import os
from sqlalchemy.orm import Session

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from app.database.connection import engine
from app.database.models import User, Admin
from app.core.auth import auth_tools
from app.database.repositories.user_repo import UserRepository
from app.database.repositories.admin_repo import AdminRepository


def init_default_users():
    """初始化默认用户和管理员"""

    db = Session(bind=engine)

    try:
        user_repo = UserRepository(db)
        admin_repo = AdminRepository(db)

        print("=" * 50)
        print("初始化默认账户...")
        print("=" * 50)

        # 创建默认用户
        default_user_username = "testuser"
        default_user_password = "123456"

        existing_user = user_repo.get_by_username(default_user_username)
        if not existing_user:
            password_hash = auth_tools.hash_password(default_user_password)
            user = user_repo.create_user(
                username=default_user_username,
                nickname=default_user_username,
                email="testuser@example.com",
                password_hash=password_hash,
                phone="13800138000",
                school="测试大学",
            )
            print(f"✓ 创建默认用户: {default_user_username}")
            print(f"  用户名: {default_user_username}")
            print(f"  密码: {default_user_password}")
            print(f"  邮箱: testuser@example.com")
        else:
            print(f"✓ 默认用户已存在: {default_user_username}")

        # 创建默认管理员
        default_admin_username = "admin"
        default_admin_password = "admin123"

        existing_admin = admin_repo.get_by_username(default_admin_username)
        if not existing_admin:
            password_hash = auth_tools.hash_password(default_admin_password)
            admin = admin_repo.create_admin(
                username=default_admin_username,
                email="admin@example.com",
                password_hash=password_hash,
                role="super_admin",
            )
            print(f"\n✓ 创建默认管理员: {default_admin_username}")
            print(f"  用户名: {default_admin_username}")
            print(f"  密码: {default_admin_password}")
            print(f"  邮箱: admin@example.com")
            print(f"  角色: 超级管理员")
        else:
            print(f"\n✓ 默认管理员已存在: {default_admin_username}")

        print("\n" + "=" * 50)
        print("初始化完成！")
        print("=" * 50)
        print("\n⚠️  请在生产环境中修改默认密码！")
        print("=" * 50)

    except Exception as e:
        print(f"\n✗ 初始化失败: {str(e)}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    init_default_users()
