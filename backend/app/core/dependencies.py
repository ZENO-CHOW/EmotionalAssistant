"""
认证依赖函数
用于从请求中提取和验证用户/管理员身份
"""

from typing import Optional
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.repositories.user_repo import UserRepository
from app.database.repositories.admin_repo import AdminRepository
from app.core.auth import auth_tools
import logging

logger = logging.getLogger(__name__)

security = HTTPBearer(auto_error=False)


async def get_current_user_id(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    authorization: Optional[str] = Header(None),
) -> int:
    """
    从请求中获取当前用户ID（不验证用户是否存在）
    供需要用户ID但不需要完整用户信息的场景使用
    """
    token = None

    if credentials:
        token = credentials.credentials
    elif authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": 401, "message": "未提供认证token"},
        )

    user_id = auth_tools.extract_user_id_from_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": 401, "message": "无效的token或token已过期"},
        )

    return user_id


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """
    从请求中获取当前用户（验证用户存在且状态正常）
    返回完整的用户对象
    """
    token = None

    if credentials:
        token = credentials.credentials
    elif authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": 401, "message": "未提供认证token"},
        )

    user_id = auth_tools.extract_user_id_from_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": 401, "message": "无效的token或token已过期"},
        )

    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 404, "message": "用户不存在"},
        )

    if str(user.status) != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": 403, "message": "用户账号已被禁用"},
        )

    return user


async def get_current_admin_id(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    authorization: Optional[str] = Header(None),
    admin_authorization: Optional[str] = Header(None, alias="Admin-Authorization"),
) -> int:
    """
    从请求中获取当前管理员ID（不验证管理员是否存在）
    供需要管理员ID但不需要完整管理员信息的场景使用
    """
    token = None

    # 优先从 Admin-Authorization header 读取（管理员专用）
    if admin_authorization and admin_authorization.startswith("Bearer "):
        token = admin_authorization.replace("Bearer ", "")
    # 如果没有，再尝试从 Authorization header 读取
    elif credentials:
        token = credentials.credentials
    elif authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": 401, "message": "未提供认证token"},
        )

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": 401, "message": "未提供认证token"},
        )
    admin_id = auth_tools.extract_admin_id_from_token(token)
    if admin_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": 401, "message": "无效的token或token已过期"},
        )

    return admin_id


async def get_current_admin(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    authorization: Optional[str] = Header(None),
    admin_authorization: Optional[str] = Header(None, alias="Admin-Authorization"),
    db: Session = Depends(get_db),
):
    """
    从请求中获取当前管理员（验证管理员存在且状态正常）
    返回完整的管理员对象
    """
    token = None

    # 优先从 Admin-Authorization header 读取（管理员专用）
    if admin_authorization and admin_authorization.startswith("Bearer "):
        token = admin_authorization.replace("Bearer ", "")
    # 如果没有，再尝试从 Authorization header 读取
    elif credentials:
        token = credentials.credentials
    elif authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": 401, "message": "未提供认证token"},
        )

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": 401, "message": "未提供认证token"},
        )
    admin_id = auth_tools.extract_admin_id_from_token(token)
    if admin_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": 401, "message": "无效的token或token已过期"},
        )

    admin_repo = AdminRepository(db)
    admin = admin_repo.get_by_id(admin_id)

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 404, "message": "管理员不存在"},
        )

    if str(admin.status) != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": 403, "message": "管理员账号已被禁用"},
        )

    return admin


async def require_super_admin(current_admin=Depends(get_current_admin)):
    """
    要求超级管理员权限
    """
    if current_admin.role != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": 403, "message": "需要超级管理员权限"},
        )
    return current_admin
