"""
数据库迁移脚本
为 users 表添加 nickname 字段
"""

import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
)

from sqlalchemy import text, inspect
from app.database.connection import engine, SessionLocal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_nickname_column():
    """添加 nickname 列到 users 表"""
    db = SessionLocal()
    try:
        inspector = inspect(engine)
        columns = inspector.get_columns("users")
        column_names = [col["name"] for col in columns]

        if "nickname" in column_names:
            logger.info("✓ nickname 列已存在，跳过添加")
            return True

        logger.info("正在添加 nickname 列...")
        alter_query = text("""
            ALTER TABLE users ADD COLUMN nickname VARCHAR(50)
        """)
        db.execute(alter_query)
        db.commit()
        logger.info("✓ 添加 nickname 列成功")

        update_query = text("""
            UPDATE users SET nickname = username WHERE nickname IS NULL
        """)
        db.execute(update_query)
        db.commit()
        logger.info("✓ 为现有用户初始化昵称为用户名")

        return True

    except Exception as e:
        db.rollback()
        logger.error(f"✗ 迁移失败: {str(e)}")
        import traceback

        traceback.print_exc()
        return False
    finally:
        db.close()


def main():
    logger.info("=" * 50)
    logger.info("开始数据库迁移: 添加 nickname 字段")
    logger.info("=" * 50)

    success = add_nickname_column()

    if success:
        logger.info("=" * 50)
        logger.info("迁移完成！")
        logger.info("=" * 50)
    else:
        logger.error("迁移失败！")
        sys.exit(1)


if __name__ == "__main__":
    main()
