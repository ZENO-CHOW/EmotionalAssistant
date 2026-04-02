"""
全局异常处理器
统一处理API异常和错误响应
"""

from typing import Optional
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)


class BusinessException(Exception):
    """业务异常基类"""

    def __init__(self, code: int, message: str, details: Optional[str] = None):
        self.code = code
        self.message = message
        self.details = details
        super().__init__(message)


class DatabaseException(BusinessException):
    """数据库异常"""

    def __init__(self, message: str, details: Optional[str] = None):
        super().__init__(500, message, details)


class ValidationException(BusinessException):
    """数据验证异常"""

    def __init__(self, message: str, details: Optional[str] = None):
        super().__init__(400, message, details)


class NotFoundException(BusinessException):
    """资源不存在异常"""

    def __init__(self, message: str = "资源不存在", details: Optional[str] = None):
        super().__init__(404, message, details)


class ConflictException(BusinessException):
    """资源冲突异常"""

    def __init__(self, message: str = "资源冲突", details: Optional[str] = None):
        super().__init__(409, message, details)


async def business_exception_handler(request: Request, exc: BusinessException):
    """业务异常处理器"""
    logger.warning(
        f"Business exception: {exc.message}, code: {exc.code}, details: {exc.details}"
    )

    return JSONResponse(
        status_code=exc.code,
        content={"code": exc.code, "message": exc.message, "details": exc.details},
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Pydantic验证异常处理器"""
    errors = []
    for error in exc.errors():
        errors.append(
            {
                "field": ".".join(str(x) for x in error["loc"]),
                "message": error["msg"],
                "type": error["type"],
            }
        )

    logger.warning(f"Validation error: {errors}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"code": 422, "message": "请求参数验证失败", "details": errors},
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """SQLAlchemy异常处理器"""
    logger.error(f"Database error: {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "数据库操作失败",
            "details": "请稍后重试或联系管理员",
        },
    )


async def general_exception_handler(request: Request, exc: Exception):
    """通用异常处理器"""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "服务器内部错误",
            "details": "请稍后重试或联系管理员",
        },
    )


def register_exception_handlers(app):
    """注册所有异常处理器"""
    app.add_exception_handler(BusinessException, business_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
