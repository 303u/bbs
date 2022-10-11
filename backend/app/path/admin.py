from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timedelta

from ..base import models, schemas
from ..core.security import hasher
from ..core.dependence import Session, get_db, check_admin


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


@router.get("/user/", response_model=list[schemas.UserOut])
async def read_users(
    skip: int = 0, db: Session = Depends(get_db),
    _: models.Users = Depends(check_admin),
) -> list[schemas.UserOut]:
    """检索所有用户"""
    return db.query(models.Users).offset(skip*40).limit(40).all()


@router.put("/user/{user_id}", response_model=schemas.Msg)
async def update_user(
    user_id: str, data: schemas.UserFull,
    db: Session = Depends(get_db),
    _: models.Users = Depends(check_admin),
) -> schemas.Msg:
    """通过id更新用户信息"""
    if not db.query(models.Users).filter(models.Users.id == user_id).first():
        raise HTTPException(404, "不存在此ID用户")
    data.password = hasher(data.password)
    if new_data := data.dict(exclude_defaults=True):
        db.query(models.Users).filter(
            models.Users.id == user_id).update(new_data)
        db.commit()
    return {}


@router.delete("/user/{user_id}", response_model=schemas.Msg)
async def delete_user(
    user_id: str, db: Session = Depends(get_db),
    _: models.Users = Depends(check_admin),
) -> schemas.Msg:
    """通过id删除用户"""
    db.query(models.Comment).filter(models.Users.id == user_id).delete()
    db.commit()
    return {}


@router.get("/item/", response_model=list[schemas.ItemFull])
async def read_items(
    skip: int = 0, db: Session = Depends(get_db),
    _: models.Users = Depends(check_admin),
) -> list[schemas.ItemFull]:
    """检索所有项目"""
    return db.query(models.Items).offset(skip*40).limit(40).all()


@router.put("/item/{item_id}", response_model=schemas.Msg)
async def update_item(
    data: schemas.ItemFull, item_id: str,
    db: Session = Depends(get_db),
    _: models.Users = Depends(check_admin),
) -> schemas.Msg:
    """通过id更新项目"""
    if new_data := data.dict(exclude_defaults=True):
        db.query(models.Items).filter(
            models.Items.id == item_id).update(new_data)
        db.commit()
    return {}


@router.delete("/item/{item_id}", response_model=schemas.Msg)
async def delete_item(
    item_id: str, db: Session = Depends(get_db),
    _: models.Users = Depends(check_admin),
) -> schemas.Msg:
    """通过id删除项目"""
    db.query(models.Items).filter(models.Items.id == item_id).delete()
    db.commit()
    return {}


@router.get("/info/", response_model=list[schemas.InfoOut])
async def read_info(
    skip: int = 0, db: Session = Depends(get_db),
    _: models.Users = Depends(check_admin),
) -> list[schemas.InfoOut]:
    """检索所有用户信息"""
    return db.query(models.Info).offset(skip*40).limit(40).all()


@router.put("/info/{info_id}", response_model=schemas.Msg)
async def update_info(
    data: schemas.InfoOut, info: str,
    db: Session = Depends(get_db),
    _: models.Users = Depends(check_admin),
) -> schemas.Msg:
    """通过id更新用户信息"""
    if new_data := data.dict(exclude_defaults=True):
        db.query(models.Info).filter(
            models.Info.id == info).update(new_data)
        db.commit()
    return {}


@router.delete("/info/{info_id}", response_model=schemas.Msg)
async def delete_info(
    info_id: str, db: Session = Depends(get_db),
    _: models.Users = Depends(check_admin),
) -> schemas.Msg:
    """通过id删除用户信息"""
    db.query(models.Info).filter(models.Info.id == info_id).delete()
    db.commit()
    return {}


@router.get("/comment/", response_model=list[schemas.CommentOut])
async def read_comment(
    skip: int = 0, db: Session = Depends(get_db),
    _: models.Users = Depends(check_admin),
) -> list[schemas.CommentOut]:
    """检索所有评论"""
    return db.query(models.Comment).offset(skip*40).limit(40).all()


@router.delete("/comment/{comment_id}", response_model=schemas.Msg)
async def delete_comment(
    comment_id: str, db: Session = Depends(get_db),
    _: models.Users = Depends(check_admin),
) -> schemas.Msg:
    """通过id删除评论"""
    db.query(models.Comment).filter(models.Comment.id == comment_id).delete()
    db.commit()
    return {}


@router.post("/banner/", response_model=schemas.Msg)
async def create_banner(
    data: schemas.Banner, db: Session = Depends(get_db),
    _: models.Users = Depends(check_admin),
) -> schemas.Msg:
    """插入推荐"""
    now = int(models.time())
    data.start = now
    data.hits = 0
    if data.end:
        data.end = now + 86400 * data.end
    db.add(models.Banner(**data.dict()))
    db.commit()
    return {}


@router.delete("/banner/{banner_id}", response_model=schemas.Msg)
async def delete_banner(
    banner_id: str, db: Session = Depends(get_db),
    _: models.Users = Depends(check_admin),
) -> schemas.Msg:
    """删除推荐"""
    db.query(models.Banner).filter(models.Banner.id == banner_id).delete()
    db.commit()
    return {}
