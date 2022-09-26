import hmac
import secrets
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import security, HTTPException

from . import Config

# OAuth2授权
reusable_oauth2 = security.OAuth2PasswordBearer(tokenUrl="/l")

# 32位的随机加密钥匙
TOKEN_KEY = secrets.token_urlsafe(32)


def hasher(password: str | None) -> str | None:
    """哈希加密"""
    return hmac.new(msg=password.encode(
        "utf8"), **Config.security).hexdigest() if password else None


def token(subject: str | int, token_key: str = TOKEN_KEY) -> str:
    """创建令牌"""
    return jwt.encode({
        "exp": datetime.utcnow() + timedelta(days=7),
        "sub": str(subject)
    }, token_key, algorithm="HS256")


def verification(subject: str | int, token_key: str = TOKEN_KEY) -> str:
    """创建验证码"""
    return jwt.encode({
        "exp": datetime.utcnow() + timedelta(minutes=5),
        "sub": str(subject)
    }, token_key, algorithm="HS256")


def verify_token(token: str, token_key: str = TOKEN_KEY) -> str:
    """验证令牌"""
    try:
        return jwt.decode(token, token_key, algorithms=["HS256"])["sub"]
    except JWTError:
        raise HTTPException(403, "身份验证无效")
