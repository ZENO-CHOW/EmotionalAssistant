"""
FastAPI主应用入口
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.database.connection import init_db
from app.database.models import Admin
from app.database.connection import SessionLocal
import bcrypt
from app.middleware.exceptions import register_exception_handlers
import logging
import os

# 配置日志
os.makedirs("./logs", exist_ok=True)
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(settings.LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="大学生情绪管理系统 API",
    description="基于DBT疗法的情绪管理辅助系统",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该配置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册全局异常处理器
register_exception_handlers(app)


def create_admin_account():
    """创建管理员账户"""
    db = SessionLocal()
    try:
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
    finally:
        db.close()


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info("=" * 50)
    logger.info("应用启动中...")
    logger.info("=" * 50)

    # 初始化数据库
    try:
        init_db()
        logger.info("✓ 数据库初始化成功")
        create_admin_account()
    except Exception as e:
        logger.error(f"✗ 数据库初始化失败: {str(e)}")

    logger.info("✓ 应用启动完成")
    logger.info("=" * 50)


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info("应用正在关闭...")


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "大学生情绪管理系统 API",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


# 导入并注册路由
from app.api import diary, chat, dbt, emotion, auth, admin

app.include_router(diary.router, prefix="/api", tags=["情绪日记"])
app.include_router(chat.router, prefix="/api", tags=["对话"])
app.include_router(dbt.router, prefix="/api", tags=["DBT技能"])
app.include_router(emotion.router, prefix="/api", tags=["情绪识别"])
app.include_router(auth.router, prefix="/api", tags=["用户认证"])
app.include_router(admin.router, prefix="/api", tags=["管理员"])

# 挂载静态文件（CAPS情绪图片）
app.mount(
    "/static",
    StaticFiles(
        directory=os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
    ),
    name="static",
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3000, reload=True)
