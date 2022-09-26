from secrets import token_hex
from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm

from ..base import models, schemas
from ..utils import recovery_code, recovery_success
from ..core.security import hasher, token, verify_token
from ..core.dependence import Session, get_db


router = APIRouter(
    prefix="/l",
    tags=["login"],
)


@router.post("/", response_model=schemas.Token)
async def login_access(
    db: Session = Depends(get_db),
    form: OAuth2PasswordRequestForm = Depends(),
) -> schemas.Token:
    """OAuth2 兼容令牌登录获取访问令牌以供将来请求使用"""
    user: models.Users = db.query(models.Users).filter(
        models.Users.email == form.username,
        models.Users.password == hasher(form.password)).first()
    if not user:
        raise HTTPException(400, "账号或密码错误")
    elif not user.active:
        raise HTTPException(400, "已被封禁用户")
    return {"access_token": token(user.id)}


@router.post("/r/{email}", response_model=schemas.VerifyCode)
async def recovery(
    email: str, db: Session = Depends(get_db)
) -> schemas.Msg:
    """发送验证序列到邮箱"""
    code = token_hex(4)
    user: models.Users = db.query(models.Users).filter(
        models.Users.email == email).first()
    if not user:
        raise HTTPException(404, "不存在此用户")
    elif not user.active:
        raise HTTPException(400, "已被封禁用户")
    recovery_code(user.email, code)
    return {"detail": "请检查邮件", "code": token(user.id, code)}


@router.post("/t/{token}", response_model=schemas.Msg)
async def reset_password(
    user_in: schemas.UserIn, token: str, code: str = Header(...),
    db: Session = Depends(get_db),
) -> schemas.Msg:
    """重设密码"""
    user: models.Users = db.query(models.Users).filter(
        models.Users.id == verify_token(code, token)).first()
    if not user or not user_in.password:
        raise HTTPException(404, "恶意行为")
    user.password = hasher(user_in.password)
    db.commit()
    recovery_success(user.email)
    return {"detail": "操作成功"}
