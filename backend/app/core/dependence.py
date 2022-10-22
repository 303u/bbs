from sqlalchemy import exc
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from ..base import models, SessionLocal
from .security import reusable_oauth2, verify_token


async def get_db() -> Session:
    """创建会话"""
    db: Session = SessionLocal()
    try:
        yield db
    except exc.OperationalError:
        raise HTTPException(400, "传参错误 或 恶意传参")
    finally:
        db.close()


async def current_user(
    db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2),
) -> models.User:
    """验证当前用户令牌"""
    user = db.query(models.User).filter(
        models.User.id == verify_token(token)).first()
    if not user:
        raise HTTPException(404, "用户不存在")
    return user


async def check_user(
    user: models.User = Depends(current_user),
) -> models.User:
    """获取当前用户"""
    if not user.active:
        raise HTTPException(400, "非激活用户")
    return user


async def check_admin(
    user: models.User = Depends(check_user),
) -> models.User:
    """获取当前管理员"""
    if not user.admin:
        raise HTTPException(400, "权限不足")
    return user


async def check_item(
    item_id: str, db: Session = Depends(get_db),
) -> models.Item:
    """获取目标项目"""
    item: models.Item = db.query(models.Item).filter(
        models.Item.id == item_id).first()
    if not item:
        raise HTTPException(404, "项目不存在")
    elif item.ban:
        raise HTTPException(400, "该项目已被封禁")
    return item
