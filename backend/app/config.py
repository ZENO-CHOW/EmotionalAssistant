"""
配置管理模块
加载环境变量和应用配置
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path


class Settings(BaseSettings):
    """应用配置类"""

    DATABASE_URL: str = "sqlite:///./data/emotions.db"
    MAX_DB_CONNECTIONS: int = 10
    DB_CONNECT_TIMEOUT: int = 30

    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    LLM_API_KEY: Optional[str] = None
    MODELSCOPE_API_KEY: Optional[str] = None
    LLM_BASE_URL: str = "https://api-inference.modelscope.cn/v1"
    LLM_MODEL: str = "ZhipuAI/GLM-4.7-Flash"
    LLM_TEMPERATURE: float = 0.3
    LLM_MAX_TOKENS: int = 500
    LLM_TIMEOUT: int = 60
    LLM_MAX_RETRIES: int = 3

    VISION_API_KEY: Optional[str] = None
    VISION_BASE_URL: str = "https://api.siliconflow.cn/v1"
    VISION_MODEL: str = "Qwen/Qwen3-VL-30B-A3B-Instruct"

    CRISIS_INTENSITY_THRESHOLD: int = 9
    CRISIS_KEYWORD_ENABLED: bool = True
    CRISIS_REPEATED_THRESHOLD: int = 3
    CRISIS_REPEATED_DAYS: int = 7

    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    CHAT_HISTORY_LIMIT: int = 20

    ENABLE_CACHE: bool = True
    CACHE_TTL_SKILLS: int = 86400
    CACHE_TTL_USER: int = 3600

    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).parent.parent / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()


settings = get_settings()
