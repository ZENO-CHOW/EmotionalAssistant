"""
添加 agent_state 字段到 chat_sessions 表
用于多AGENT状态持久化
"""

from sqlalchemy import text
from app.database.connection import get_db


def run_migration():
    """执行迁移"""
    db = next(get_db())

    try:
        result = db.execute(
            text("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = 'chat_sessions' AND column_name = 'agent_state'
        """)
        )
        exists = result.fetchone()

        if exists:
            print("agent_state 字段已存在，跳过迁移")
        else:
            db.execute(
                text("""
                ALTER TABLE chat_sessions ADD COLUMN agent_state TEXT
            """)
            )
            db.commit()
            print("成功添加 agent_state 字段")

    except Exception as e:
        db.rollback()
        print(f"迁移失败: {e}")
        raise


if __name__ == "__main__":
    run_migration()
