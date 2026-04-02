"""
用户认证API路由
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
import logging

from app.database.connection import get_db
from app.database.repositories.user_repo import UserRepository
from app.core.auth import auth_tools
from app.core.dependencies import get_current_user, get_current_user_id

logger = logging.getLogger(__name__)
router = APIRouter()


class LoginRequest(BaseModel):
    """登录请求"""

    username: str = Field(..., min_length=3, max_length=50, description="用户名或邮箱")
    password: str = Field(..., min_length=6, max_length=100, description="密码")


class RegisterRequest(BaseModel):
    """注册请求"""

    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: Optional[EmailStr] = Field(None, description="邮箱")
    password: str = Field(..., min_length=6, max_length=100, description="密码")
    confirmPassword: str = Field(
        ..., min_length=6, max_length=100, description="确认密码"
    )
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    school: Optional[str] = Field(None, max_length=100, description="学校")

    @validator("confirmPassword")
    def passwords_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("两次密码不一致")
        return v


class ChangePasswordRequest(BaseModel):
    """修改密码请求"""

    currentPassword: str = Field(
        ..., min_length=6, max_length=100, description="当前密码"
    )
    newPassword: str = Field(..., min_length=6, max_length=100, description="新密码")


class UpdateProfileRequest(BaseModel):
    """更新个人信息请求"""

    nickname: Optional[str] = Field(
        None, min_length=1, max_length=50, description="昵称"
    )
    email: Optional[EmailStr] = Field(None, description="邮箱")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    school: Optional[str] = Field(None, max_length=100, description="学校")
    avatar: Optional[str] = Field(None, description="头像URL")


class LoginResponse(BaseModel):
    """登录响应"""

    code: int = 200
    message: str = "登录成功"
    data: dict


class RegisterResponse(BaseModel):
    """注册响应"""

    code: int = 200
    message: str = "注册成功"
    data: dict


class UserInfoResponse(BaseModel):
    """用户信息响应"""

    code: int = 200
    message: str = "获取成功"
    data: dict


@router.post("/auth/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    用户登录

    支持用户名或邮箱登录
    """
    try:
        user_repo = UserRepository(db)

        user = user_repo.get_by_username_or_email(request.username)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": 401, "message": "用户名或密码错误"},
            )

        if not auth_tools.verify_password(request.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": 401, "message": "用户名或密码错误"},
            )

        if user.status != "active":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": 403, "message": "账号已被禁用"},
            )

        user_repo.update_last_login(user.id)

        token = auth_tools.create_user_token(user.id, user.username)

        logger.info(f"用户 {user.username} (ID: {user.id}) 登录成功")

        return LoginResponse(
            data={
                "token": token,
                "userInfo": {
                    "id": user.id,
                    "username": user.username,
                    "nickname": user.nickname,
                    "email": user.email,
                    "phone": user.phone,
                    "school": user.school,
                    "avatar": user.avatar,
                },
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"登录失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": "登录失败，请稍后重试"},
        )


@router.post("/auth/register", response_model=RegisterResponse)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    用户注册
    """
    try:
        user_repo = UserRepository(db)

        if user_repo.check_username_exists(request.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"code": 409, "message": "用户名已存在"},
            )

        if request.email and user_repo.check_email_exists(request.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"code": 409, "message": "邮箱已被注册"},
            )

        password_hash = auth_tools.hash_password(request.password)

        user = user_repo.create_user(
            username=request.username,
            nickname=request.username,
            email=request.email,
            password_hash=password_hash,
            phone=request.phone,
            school=request.school,
        )

        logger.info(f"新用户 {user.username} (ID: {user.id}) 注册成功")

        return RegisterResponse(
            data={"userId": user.id, "username": user.username, "email": user.email}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"注册失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": "注册失败，请稍后重试"},
        )


@router.get("/auth/user", response_model=UserInfoResponse)
async def get_user_info(current_user=Depends(get_current_user)):
    """
    获取当前用户信息
    """
    try:
        return UserInfoResponse(
            data={
                "id": current_user.id,
                "username": current_user.username,
                "nickname": current_user.nickname,
                "email": current_user.email,
                "phone": current_user.phone,
                "school": current_user.school,
                "avatar": current_user.avatar,
                "status": current_user.status,
                "createdAt": current_user.created_at.isoformat()
                if current_user.created_at
                else None,
                "lastLoginAt": current_user.last_login_at.isoformat()
                if current_user.last_login_at
                else None,
            }
        )
    except Exception as e:
        logger.error(f"获取用户信息失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": "获取用户信息失败"},
        )


@router.put("/auth/user", response_model=UserInfoResponse)
async def update_user_info(
    request: UpdateProfileRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    更新用户信息
    """
    try:
        user_repo = UserRepository(db)

        updates = {}

        if request.nickname is not None:
            updates["nickname"] = request.nickname

        if request.email is not None:
            if request.email != current_user.email:
                if user_repo.check_email_exists(request.email):
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail={"code": 409, "message": "邮箱已被使用"},
                    )
            updates["email"] = request.email

        if request.phone is not None:
            updates["phone"] = request.phone

        if request.school is not None:
            updates["school"] = request.school

        if request.avatar is not None:
            updates["avatar"] = request.avatar

        if updates:
            user_repo.update_user(current_user.id, updates)
            user = user_repo.get_by_id(current_user.id)
        else:
            user = current_user

        logger.info(f"用户 {user.username} (ID: {user.id}) 更新信息")

        return UserInfoResponse(
            data={
                "id": user.id,
                "username": user.username,
                "nickname": user.nickname,
                "email": user.email,
                "phone": user.phone,
                "school": user.school,
                "avatar": user.avatar,
                "status": user.status,
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新用户信息失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": "更新用户信息失败"},
        )


@router.post("/auth/change-password")
async def change_password(
    request: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    修改密码
    """
    try:
        if not auth_tools.verify_password(
            request.currentPassword, current_user.password_hash
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": 401, "message": "当前密码错误"},
            )

        new_password_hash = auth_tools.hash_password(request.newPassword)

        user_repo = UserRepository(db)
        user_repo.update_password(current_user.id, new_password_hash)

        logger.info(f"用户 {current_user.username} (ID: {current_user.id}) 修改密码")

        return {"code": 200, "message": "密码修改成功"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"修改密码失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": "修改密码失败"},
        )


@router.post("/auth/logout")
async def logout(user_id: int = Depends(get_current_user_id)):
    """
    用户退出登录

    注意：由于使用无状态的JWT token，退出登录主要在客户端清除token
    后端可以添加token黑名单机制（可选）
    """
    try:
        logger.info(f"用户ID: {user_id} 退出登录")
        return {"code": 200, "message": "退出成功"}
    except Exception as e:
        logger.error(f"退出登录失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": "退出登录失败"},
        )
