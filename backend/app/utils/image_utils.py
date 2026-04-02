import base64
import os
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def get_static_dir() -> str:
    """获取 static 目录的完整路径"""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "static")


def resolve_image_path(image_url: str) -> str:
    """
    将相对路径解析为完整的文件系统路径

    Args:
        image_url: 图片URL（可能是相对路径或绝对路径）

    Returns:
        完整的文件系统路径

    Raises:
        FileNotFoundError: 如果图片文件不存在
        ValueError: 如果URL格式不支持
    """
    if image_url.startswith("/static/"):
        relative_path = image_url[8:]  # 移除 /static/
        full_path = os.path.join(get_static_dir(), relative_path)

        if not Path(full_path).exists():
            raise FileNotFoundError(f"图片文件不存在: {full_path}")

        return full_path

    # 如果已经是完整路径，直接返回
    if Path(image_url).exists():
        return image_url

    raise ValueError(f"不支持的图片URL格式: {image_url}")


def load_image_as_data_url(image_url: str) -> str:
    """
    将本地图片路径转换为 data URL 格式
    参考 test_vision.py:14-25 的实现

    Args:
        image_url: 图片URL（相对路径或绝对路径）

    Returns:
        data URL 格式: data:image/jpeg;base64,...

    Raises:
        FileNotFoundError: 如果图片文件不存在
    """
    # 解析为完整路径
    image_path = resolve_image_path(image_url)

    # 读取图片文件并编码为 base64
    with open(image_path, "rb") as f:
        image_data = f.read()
        base64_encoded = base64.b64encode(image_data).decode("utf-8")

    # 根据文件扩展名确定 MIME 类型
    if image_path.endswith(".png"):
        mime_type = "image/png"
    else:
        mime_type = "image/jpeg"

    data_url = f"data:{mime_type};base64,{base64_encoded}"
    logger.debug(f"图片已转换为 data URL，长度: {len(data_url)}")

    return data_url
