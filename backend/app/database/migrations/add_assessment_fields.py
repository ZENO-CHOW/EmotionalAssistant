"""
添加情绪评估字段到chat_sessions表
"""
import sqlite3
import os

def run_migration():
    """执行数据库迁移"""
    # 获取数据库路径
    db_path = os.path.join(os.path.dirname(__file__), "../../../data/emotions.db")

    if not os.path.exists(db_path):
        print(f"数据库文件不存在: {db_path}")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 检查字段是否已存在
        cursor.execute("PRAGMA table_info(chat_sessions)")
        columns = [col[1] for col in cursor.fetchall()]

        # 添加assessment_status字段
        if "assessment_status" not in columns:
            cursor.execute("""
                ALTER TABLE chat_sessions
                ADD COLUMN assessment_status VARCHAR(20) DEFAULT 'not_started' NOT NULL
            """)
            print("✓ 添加assessment_status字段")
        else:
            print("- assessment_status字段已存在")

        # 添加assessment_data字段
        if "assessment_data" not in columns:
            cursor.execute("""
                ALTER TABLE chat_sessions
                ADD COLUMN assessment_data TEXT
            """)
            print("✓ 添加assessment_data字段")
        else:
            print("- assessment_data字段已存在")

        conn.commit()
        conn.close()

        print("\n✅ 数据库迁移完成")
        return True

    except Exception as e:
        print(f"\n❌ 数据库迁移失败: {str(e)}")
        return False

if __name__ == "__main__":
    run_migration()
