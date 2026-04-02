"""
认证工具模块
提供密码加密和JWT token生成/验证功能
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
import bcrypt
from app.config import settings


class AuthTools:
    """认证工具类"""

    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    def hash_password(self, password: str) -> str:
        """加密密码"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )

    def create_access_token(
        self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None
    ) -> str:
        """创建访问token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=self.access_token_expire_minutes
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_access_token(self, token: str) -> Optional[Dict[str, Any]]:
        """解码访问token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None

    def create_user_token(self, user_id: int, username: str) -> str:
        """创建用户token"""
        return self.create_access_token(
            data={"sub": str(user_id), "username": username, "type": "user"}
        )

    def create_admin_token(
        self, admin_id: int, username: str, role: str = "admin"
    ) -> str:
        """创建管理员token"""
        return self.create_access_token(
            data={
                "sub": str(admin_id),
                "username": username,
                "role": role,
                "type": "admin",
            }
        )

    def extract_user_id_from_token(self, token: str) -> Optional[int]:
        """从token中提取用户ID"""
        payload = self.decode_access_token(token)
        if payload and payload.get("type") == "user":
            try:
                sub = payload.get("sub")
                if sub is not None:
                    return int(sub)
                return None
            except (ValueError, TypeError):
                return None
        return None

    def extract_admin_id_from_token(self, token: str) -> Optional[int]:
        """从token中提取管理员ID"""
        payload = self.decode_access_token(token)
        if payload and payload.get("type") == "admin":
            try:
                sub = payload.get("sub")
                if sub is not None:
                    return int(sub)
                return None
            except (ValueError, TypeError):
                return None
        return None


auth_tools = AuthTools()
