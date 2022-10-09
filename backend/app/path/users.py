from secrets import token_hex
from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.exc import SQLAlchemyError

from ..base import models, schemas
from ..utils import new_account, get_code_email
from ..core.security import hasher, token, verify_token
from ..core.dependence import Session, get_db, check_user


router = APIRouter(
    prefix="/users",
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
    if db.query(models.Users).filter(models.Users.email == data.email).first():
        raise HTTPException(400, "请更换邮箱")
    data.password = hasher(data.password)

    try:
        user = models.Users(**data.dict())
        # 创建用户
        db.add(user)
        db.commit()
        # 刷新用户信息
        db.refresh(user)
        # 发送邮件到用户
        new_account(data.email, data.name)
    except SQLAlchemyError:
        # id 碰撞
        return {"detail": "繁忙请重试"}
    except Exception:
        # 创建成功但邮箱为空
        db.delete(user)
        db.commit()
        return {"detail": "无法访问的邮箱"}

    # 默认创建用户空信息
    db.add(models.Info(id=user.id))
    db.commit()
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
    db.query(models.Users).filter(models.Users.id == user.id).update(data)
    db.commit()
    return {"detail": "操作成功"}


@router.delete("/", response_model=schemas.Msg)
async def cancel_user(
    db: Session = Depends(get_db),
    user: models.Users = Depends(check_user),
) -> schemas.Msg:
    """申请注销账号"""
    for item in db.query(models.Items).filter(
            models.Items.author == user.id).all():
        item: models.Items
        db.query(models.Comment).filter(
            models.Comment.item == item.id).delete()
        db.delete(item)
    db.query(models.Comment).filter(
        models.Items.author == user.id).delete()
    db.query(models.Info).filter(
        models.Info.id == user.id).delete()
    db.delete(user)
    db.commit()
    return {"detail": "操作成功"}


@router.post("/t", response_model=schemas.VerifyCode)
async def get_code(
    user: models.Users = Depends(check_user),
) -> schemas.VerifyCode:
    """获取验证码"""
    code = token_hex(4)
    get_code_email(user.email, code)
    return {"detail": "请检查邮件", "code": token(user.id, code, 0.1)}


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
