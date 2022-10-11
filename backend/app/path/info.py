from fastapi import APIRouter, HTTPException, Depends, Body

from ..base import models, schemas
from ..core.dependence import Session, get_db, check_user


router = APIRouter(
    prefix="/info",
    tags=["info"],
)


@router.get("/{user_id}", response_model=schemas.InfoOut)
async def user_info(
    user_id: str,
    db: Session = Depends(get_db),
    _: models.Users = Depends(check_user),
) -> schemas.InfoOut:
    """获取用户信息"""
    info: models.Info = db.query(models.Info).filter(
        models.Info.id == user_id).first()
    if info:
        return info
    elif db.query(models.Users).filter(
            models.Users.id == user_id).first():
        # 若用户存在
        info = models.Info(id=user_id)
        db.add(info)
        db.commit()
        db.refresh(info)
        return info
    raise HTTPException(404, "用户信息不存在")


@router.put("/", response_model=schemas.Msg)
async def update_user(
    data: schemas.InfoIn,
    db: Session = Depends(get_db),
    user: models.Users = Depends(check_user),
) -> schemas.Msg:
    """更新用户信息"""
    db.query(models.Info).filter(models.Info.id == user.id).update(
        data.dict(exclude_defaults=True))
    db.commit()
    return {}


@router.patch("/phone", response_model=schemas.Msg)
async def update_phone(
    data: str = Body(None),
    db: Session = Depends(get_db),
    user: models.Users = Depends(check_user),
) -> schemas.Msg:
    """更新联系电话"""
    db.query(models.Info).filter(models.Info.id == user.id).update(
        {"phone": data})
    db.commit()
    return {}
