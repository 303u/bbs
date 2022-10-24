from secrets import token_hex
from fastapi import APIRouter, HTTPException, Depends, Header

from ..base import models, schemas
from ..utils import new_account, get_code_email
from ..core.security import hasher, token, verify_token
from ..core.dependence import Session, get_db, check_user


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/", response_model=schemas.InfoOut)
async def read_user(
    user: models.User = Depends(check_user),
) -> schemas.InfoOut:
    """获取用户自身"""
    return user.info


@router.post("/", response_model=schemas.Msg)
async def create_user(
    data: schemas.UserIn,
    db: Session = Depends(get_db),
) -> schemas.Msg:
    """创建新用户"""
    if db.query(models.User).filter(models.User.email == data.email).first():
        raise HTTPException(400, "请更换邮箱")

    user = models.User()
    user.email = data.email
    user.password = hasher(data.password)

    try:
        # 创建用户
        db.add(user)
        db.commit()
        # 刷新用户信息
        db.refresh(user)
        # 发送邮件到用户
        new_account(data.email, data.name)
    except Exception:
        # 创建成功但邮箱无法收件
        db.delete(user)
        db.commit()
        return {"detail": "无法访问的邮箱"}

    # 默认创建用户空信息
    db.add(models.Info(id=user.id, name=data.name))
    db.commit()
    return {}


@router.put("/", response_model=schemas.Msg)
async def update_user(
    data: schemas.UserIn, token: str, code: str = Header(...),
    db: Session = Depends(get_db),
    user: models.User = Depends(check_user),
) -> schemas.Msg:
    """更新用户信息"""
    if data.password or data.email:
        try:
            assert user.id == verify_token(code, token)
        except Exception:
            raise HTTPException(400, "验证码无效或失效")
    if data.name:
        user.info.name = data.name
    if data.password:
        user.password = hasher(data.password)
    if data.email:
        user.email = data.email
    db.commit()
    return {}


@router.delete("/", response_model=schemas.Msg)
async def cancel_user(
    db: Session = Depends(get_db),
    user: models.User = Depends(check_user),
) -> schemas.Msg:
    """申请注销账号"""
    user.active = 0
    db.commit()
    return {}


@router.post("/token", response_model=schemas.VerifyCode)
async def get_code(
    user: models.User = Depends(check_user),
) -> schemas.VerifyCode:
    """获取验证码"""
    code = token_hex(4)
    get_code_email(user.email, code)
    return {"detail": "请检查邮件", "code": token(user.id, code, 0.1)}


@router.get("/{user_id}", response_model=schemas.UserOut)
async def read_user(
    user_id: str,
    db: Session = Depends(get_db),
    _: models.User = Depends(check_user),
) -> schemas.UserOut:
    """获取用户信息"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        return user
    raise HTTPException(404)
