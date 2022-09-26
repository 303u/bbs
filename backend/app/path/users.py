from secrets import token_hex
from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.exc import SQLAlchemyError

from ..base import models, schemas
from ..utils import new_account, get_code_email
from ..core.security import hasher, verification, verify_token
from ..core.dependence import Session, get_db, check_user


router = APIRouter(
    prefix="/u",
    tags=["users"],
)


@router.get("/", response_model=schemas.UserOut)
async def read_user(
    user: models.Users = Depends(check_user),
) -> schemas.UserOut:
    """获取用户自身"""
    return user


@router.post("/", response_model=schemas.Msg)
async def create_user(
    data: schemas.UserIn,
    db: Session = Depends(get_db),
) -> schemas.Msg:
    """创建新用户"""
    if db.query(models.Users).filter_by(email=data.email).first():
        raise HTTPException(400, "请更换邮箱")
    data.password = hasher(data.password)

    try:
        db.add(models.Users(**data.dict()))
        db.commit()
    except SQLAlchemyError:
        return {"detail": "请重试"}

    new_account(data.email, data.name)
    return {"detail": "创建成功"}


@router.put("/", response_model=schemas.Msg)
async def update_user(
    data: schemas.UserIn, token: str, code: str = Header(...),
    db: Session = Depends(get_db),
    user: models.Users = Depends(check_user),
) -> schemas.Msg:
    """更新用户信息"""
    if data.password or data.email:
        try:
            assert user.id == verify_token(code, token)
        except Exception:
            raise HTTPException(400, "验证码无效或失效")
    data.password = hasher(data.password)
    data = data.dict(exclude_defaults=True) | {"info": None}
    db.query(models.Users).filter_by(id=user.id).update(data)
    db.commit()
    return {"detail": "操作成功"}


@router.delete("/", response_model=schemas.Msg)
async def cancel_user(
    db: Session = Depends(get_db),
    user: models.Users = Depends(check_user),
) -> schemas.Msg:
    """申请注销账号"""
    db.query(models.Items).filter_by(author=user.id).delete()
    db.query(models.Talks).filter_by(author=user.id).delete()
    db.delete(user)
    db.commit()
    return {"detail": "操作成功"}


@router.post("/t", response_model=schemas.VerifyCode)
async def get_code(
    user: models.Users = Depends(check_user),
) -> schemas.VerifyCode:
    """获取验证码"""
    code = token_hex(4)
    get_code_email(user.email, "验证码", code)
    return {"detail": "请检查邮件", "code": verification(user.id, code)}


@router.get("/{user_id}", response_model=schemas.UserOut)
async def read_user(
    user_id: str,
    db: Session = Depends(get_db),
    _: models.Users = Depends(check_user),
) -> schemas.UserOut:
    """获取用户信息"""
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user:
        return user
    raise HTTPException(404)
