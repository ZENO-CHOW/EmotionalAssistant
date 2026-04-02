"""
数据库初始化脚本
创建所有表和初始数据
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
)

from app.database.connection import init_db, engine
from app.database.models import User, Admin
from sqlalchemy.orm import Session
import bcrypt
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_admin(db: Session):
    """创建管理员账户"""
    admin = db.query(Admin).filter(Admin.username == "admin").first()
    if not admin:
        hashed_password = bcrypt.hashpw(
            "admin123".encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        admin = Admin(
            username="admin",
            email="admin@example.com",
            password_hash=hashed_password,
            role="super_admin",
        )
        db.add(admin)
        db.commit()
        logger.info("✓ 创建管理员账户: admin (密码: admin123)")
    else:
        logger.info("✓ 管理员账户已存在")


def create_test_user(db: Session):
    """创建测试用户"""
    test_user = db.query(User).filter(User.username == "testuser").first()
    if not test_user:
        hashed_password = bcrypt.hashpw(
            "test123456".encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        test_user = User(
            username="testuser",
            nickname="测试同学",
            email="test@example.com",
            password_hash=hashed_password,
            school="测试大学",
            status="active",
        )
        db.add(test_user)
        db.commit()
        logger.info("✓ 创建测试用户: testuser (密码: test123456)")
    else:
        logger.info("✓ 测试用户已存在")


def main():
    """主函数"""
    try:
        logger.info("=" * 50)
        logger.info("开始初始化数据库...")
        logger.info("=" * 50)

        # 初始化数据库（创建所有表）
        init_db()
        logger.info("✓ 数据库表创建成功")

        # 创建测试数据
        from app.database.connection import SessionLocal

        db = SessionLocal()
        try:
            create_test_user(db)
            create_admin(db)
        finally:
            db.close()

        logger.info("=" * 50)
        logger.info("数据库初始化完成！")
        logger.info("=" * 50)
        logger.info("\n测试账号信息：")
        logger.info("  用户名: testuser")
        logger.info("  密码: test123456")
        logger.info("  邮箱: test@example.com")
        logger.info("\n管理员账号信息：")
        logger.info("  用户名: admin")
        logger.info("  密码: admin123")
        logger.info("  邮箱: admin@example.com")

    except Exception as e:
        logger.error(f"✗ 数据库初始化失败: {str(e)}")
        raise


if __name__ == "__main__":
    main()
