"""
管理员认证API路由
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime, timezone

from app.database.connection import get_db
from app.database.repositories.admin_repo import AdminRepository
from app.database.repositories.user_repo import UserRepository
from app.database.repositories.diary_repo import DiaryRepository
from app.database.repositories.crisis_repo import CrisisRepository
from app.core.auth import auth_tools
from app.core.dependencies import (
    get_current_admin,
    get_current_admin_id,
    require_super_admin,
)

logger = logging.getLogger(__name__)
router = APIRouter()


class AdminLoginRequest(BaseModel):
    """管理员登录请求"""

    username: str = Field(
        ..., min_length=3, max_length=50, description="管理员账号或邮箱"
    )
    password: str = Field(..., min_length=6, max_length=100, description="密码")
    remember: Optional[bool] = Field(False, description="是否记住登录（7天）")


class AdminLoginResponse(BaseModel):
    """管理员登录响应"""

    code: int = 200
    message: str = "登录成功"
    data: dict


class AdminInfoResponse(BaseModel):
    """管理员信息响应"""

    code: int = 200
    message: str = "获取成功"
    data: dict


@router.post("/admin/login", response_model=AdminLoginResponse)
async def admin_login(request: AdminLoginRequest, db: Session = Depends(get_db)):
    """
    管理员登录

    支持用户名或邮箱登录
    """
    try:
        admin_repo = AdminRepository(db)

        admin = admin_repo.get_by_username_or_email(request.username)

        if not admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": 401, "message": "管理员账号或密码错误"},
            )

        if not auth_tools.verify_password(request.password, str(admin.password_hash)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": 401, "message": "管理员账号或密码错误"},
            )

        if admin.status != "active":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": 403, "message": "管理员账号已被禁用"},
            )

        admin_repo.update_last_login(admin.id)

        token = auth_tools.create_admin_token(admin.id, admin.username, admin.role)

        logger.info(
            f"管理员 {admin.username} (ID: {admin.id}, Role: {admin.role}) 登录成功"
        )

        return AdminLoginResponse(
            data={
                "token": token,
                "adminInfo": {
                    "id": admin.id,
                    "username": admin.username,
                    "email": admin.email,
                    "role": admin.role,
                    "status": admin.status,
                },
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"管理员登录失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": "登录失败，请稍后重试"},
        )


@router.post("/admin/logout")
async def admin_logout(admin_id: int = Depends(get_current_admin_id)):
    """
    管理员退出登录
    """
    try:
        logger.info(f"管理员ID: {admin_id} 退出登录")
        return {"code": 200, "message": "退出成功"}
    except Exception as e:
        logger.error(f"管理员退出登录失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": "退出登录失败"},
        )


@router.get("/admin/info", response_model=AdminInfoResponse)
async def get_admin_info(current_admin=Depends(get_current_admin)):
    """
    获取当前管理员信息
    """
    try:
        return AdminInfoResponse(
            data={
                "id": current_admin.id,
                "username": current_admin.username,
                "email": current_admin.email,
                "role": current_admin.role,
                "status": current_admin.status,
                "lastLoginAt": current_admin.last_login_at.isoformat()
                if current_admin.last_login_at
                else None,
                "createdAt": current_admin.created_at.isoformat()
                if current_admin.created_at
                else None,
            }
        )
    except Exception as e:
        logger.error(f"获取管理员信息失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": "获取管理员信息失败"},
        )


@router.get("/admin/statistics/overview")
async def get_statistics_overview(
    db: Session = Depends(get_db), current_admin=Depends(get_current_admin)
):
    """
    获取数据统计概览

    包含用户统计、管理员统计、情绪分析统计、危机统计等
    """
    try:
        user_repo = UserRepository(db)
        admin_repo = AdminRepository(db)
        diary_repo = DiaryRepository(db)
        crisis_repo = CrisisRepository(db)

        user_stats = user_repo.get_user_statistics()
        admin_stats = admin_repo.get_admin_statistics()
        today_active_users = user_repo.get_today_active_users()
        total_diaries = diary_repo.get_total_diary_count()
        pending_crisis_count = crisis_repo.get_pending_crisis_count()

        return {
            "code": 200,
            "message": "获取成功",
            "data": {
                "users": user_stats,
                "admins": admin_stats,
                "todayActiveUsers": today_active_users,
                "totalDiaries": total_diaries,
                "pendingCrisisCount": pending_crisis_count,
            },
        }
    except Exception as e:
        logger.error(f"获取统计概览失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": "获取统计概览失败"},
        )


@router.get("/admin/statistics/emotions")
async def get_emotion_statistics(
    period: str = "week",
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """
    获取情绪分布统计

    参数:
    - period: 时间范围 (week/month/year)
    """
    try:
        diary_repo = DiaryRepository(db)

        from datetime import date, timedelta

        end_date = date.today()
        if period == "week":
            start_date = end_date - timedelta(days=6)
        elif period == "month":
            start_date = end_date - timedelta(days=29)
        elif period == "year":
            start_date = end_date - timedelta(days=364)
        else:
            start_date = end_date - timedelta(days=6)

        distribution = diary_repo.get_global_emotion_distribution(
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
        )

        return {"code": 200, "message": "获取成功", "data": distribution}
    except Exception as e:
        logger.error(f"获取情绪统计失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": "获取情绪统计失败"},
        )


@router.get("/admin/statistics/user-activity")
async def get_user_activity_statistics(
    period: str = "week",
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """
    获取用户活跃度统计

    参数:
    - period: 时间范围 (week/month)
    """
    try:
        user_repo = UserRepository(db)

        from datetime import date, timedelta

        end_date = date.today()
        if period == "week":
            start_date = end_date - timedelta(days=6)
        elif period == "month":
            start_date = end_date - timedelta(days=29)
        else:
            start_date = end_date - timedelta(days=6)

        daily_active_users = user_repo.get_daily_active_users_count(
            start_date=start_date, end_date=end_date
        )

        return {"code": 200, "message": "获取成功", "data": daily_active_users}
    except Exception as e:
        logger.error(f"获取用户活跃度统计失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": "获取用户活跃度统计失败"},
        )


@router.get("/admin/users")
async def get_user_list(
    keyword: Optional[str] = None,
    status: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """
    获取用户列表

    参数:
    - keyword: 搜索关键词（用户名、邮箱、手机号、学校）
    - status: 用户状态筛选 (active/inactive)
    - page: 页码
    - page_size: 每页数量
    """
    try:
        user_repo = UserRepository(db)

        users, total = user_repo.list_users(
            status=status, keyword=keyword, page=page, page_size=page_size
        )

        user_list = []
        for user in users:
            emotion_count = user_repo.get_user_diary_count(user.id)
            risk_level = user_repo.get_user_risk_level(user.id)

            user_list.append(
                {
                    "id": user.id,
                    "name": user.nickname or user.username,
                    "username": user.username,
                    "email": user.email,
                    "phone": user.phone,
                    "school": user.school,
                    "avatar": user.avatar,
                    "status": user.status,
                    "registerTime": user.created_at.strftime("%Y-%m-%d")
                    if user.created_at
                    else None,
                    "lastActive": _format_relative_time(user.last_login_at)
                    if user.last_login_at
                    else "从未登录",
                    "emotionCount": emotion_count,
                    "riskLevel": risk_level,
                }
            )

        total_pages = (total + page_size - 1) // page_size

        return {
            "code": 200,
            "message": "获取成功",
            "data": {
                "list": user_list,
                "total": total,
                "page": page,
                "pageSize": page_size,
                "totalPages": total_pages,
            },
        }
    except Exception as e:
        logger.error(f"获取用户列表失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"code": 500, "message": "获取用户列表失败"},
        )


def _format_relative_time(dt: datetime) -> str:
    """
    格式化为相对时间
    :param dt: datetime 对象
    :return: 相对时间字符串
    """
    now = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    diff = now - dt
    diff_seconds = int(diff.total_seconds())

    if diff_seconds < 60:
        return "刚刚"
    elif diff_seconds < 3600:
        minutes = diff_seconds // 60
        return f"{minutes}分钟前"
    elif diff_seconds < 86400:
        hours = diff_seconds // 3600
        return f"{hours}小时前"
    elif diff_seconds < 2592000:
        days = diff_seconds // 86400
        return f"{days}天前"
    else:
        return dt.strftime("%Y-%m-%d")


@router.get("/admin/users/{user_id}")
async def get_user_detail(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """
    获取用户详情
    """
    try:
        user_repo = UserRepository(db)
        user = user_repo.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": 404, "message": "用户不存在"},
            )

        return {
            "code": 200,
            "message": "获取成功",
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "school": user.school,
                "avatar": user.avatar,
                "status": user.status,
                "createdAt": user.created_at.isoformat() if user.created_at else None,
                "lastLoginAt": user.last_login_at.isoformat()
                if user.last_login_at
                else None,
            },
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取用户详情失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": "获取用户详情失败"},
        )


@router.put("/admin/users/{user_id}/status")
async def update_user_status(
    user_id: int,
    status_data: Dict[str, str],
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """
    更新用户状态

    参数:
    - status: 状态 (active/inactive/suspended)
    - reason: 状态变更原因（可选）
    """
    try:
        user_repo = UserRepository(db)

        new_status = status_data.get("status")
        if new_status not in ["active", "inactive", "suspended"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": 400, "message": "无效的状态值"},
            )

        success = user_repo.change_user_status(user_id, new_status)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": 404, "message": "用户不存在"},
            )

        logger.info(
            f"管理员 {current_admin.username} 将用户 {user_id} 状态改为 {new_status}"
        )

        return {"code": 200, "message": "状态更新成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新用户状态失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": "更新用户状态失败"},
        )


@router.delete("/admin/users/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(require_super_admin),
):
    """
    删除用户（仅超级管理员）

    警告：此操作不可逆，将删除用户所有数据
    """
    try:
        user_repo = UserRepository(db)

        success = user_repo.delete_user(user_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": 404, "message": "用户不存在"},
            )

        logger.warning(f"超级管理员 {current_admin.username} 删除了用户 {user_id}")

        return {"code": 200, "message": "删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除用户失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": "删除用户失败"},
        )


@router.get("/admin/crisis/recent")
async def get_recent_crisis_events(
    limit: int = 10,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """
    获取最近的危机事件列表

    参数:
    - limit: 返回数量限制（默认10）
    - status: 状态筛选 (pending/handling/resolved)
    """
    try:
        crisis_repo = CrisisRepository(db)
        user_repo = UserRepository(db)

        crisis_events = crisis_repo.list_recent_crisis_events(
            limit=limit, status=status
        )

        crisis_list = []
        for crisis in crisis_events:
            user = user_repo.get_by_id(crisis.user_id)

            level_map = {"high": "high", "medium": "medium", "low": "low"}
            level_icon_map = {"high": "🔴", "medium": "🟡", "low": "🟢"}
            level_text_map = {"high": "高危", "medium": "中危", "low": "低危"}
            risk_level_str = (
                str(crisis.risk_level) if crisis.risk_level is not None else "low"
            )

            crisis_list.append(
                {
                    "id": crisis.id,
                    "level": level_map.get(risk_level_str, "low"),
                    "levelIcon": level_icon_map.get(risk_level_str, "🟢"),
                    "levelText": level_text_map.get(risk_level_str, "低危"),
                    "userName": user.nickname or user.username
                    if user is not None
                    else f"用户{crisis.user_id}",
                    "userId": crisis.user_id,
                    "description": crisis.trigger_reason,
                    "emotionIntensity": crisis.emotion_intensity,
                    "time": _format_relative_time(crisis.created_at),
                    "handled": str(crisis.status) != "pending",
                }
            )

        return {"code": 200, "message": "获取成功", "data": crisis_list}
    except Exception as e:
        logger.error(f"获取最近危机事件失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"code": 500, "message": "获取危机事件失败"},
        )
