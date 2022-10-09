from fastapi import APIRouter, HTTPException, Depends

from ..base import models, schemas
from ..core.security import hasher
from ..core.dependence import Session, get_db, check_admin


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


@router.get("/u/", response_model=list[schemas.UserOut])
async def read_users(
    skip: int = 0, db: Session = Depends(get_db),
    _: models.Users = Depends(check_admin),
) -> list[schemas.UserOut]:
    """检索所有用户"""
    return db.query(models.Users).offset(skip*40).limit(40).all()


@router.put("/u/{user_id}", response_model=schemas.Msg)
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
    return {"detail": "操作成功"}


@router.delete("/u/{user_id}", response_model=schemas.Msg)
async def delete_user(
    user_id: str, db: Session = Depends(get_db),
    _: models.Users = Depends(check_admin),
) -> schemas.Msg:
    """通过id删除用户"""
    db.query(models.Comment).filter(models.Users.id==user_id).delete()
    db.commit()
    return {"detail": "操作成功"}


@router.get("/i/", response_model=list[schemas.ItemFull])
async def read_items(
    skip: int = 0, db: Session = Depends(get_db),
    _: models.Users = Depends(check_admin),
) -> list[schemas.ItemFull]:
    """检索所有项目"""
    return db.query(models.Items).offset(skip*40).limit(40).all()


@router.put("/i/{item_id}", response_model=schemas.Msg)
async def update_item(
    data: schemas.ItemFull, item_id: str,
    db: Session = Depends(get_db),
    _: models.Users = Depends(check_admin),
) -> schemas.Msg:
    """通过id更新项目"""
    if new_data := data.dict(exclude_defaults=True):
        db.query(models.Items).filter(models.Items.id==item_id).update(new_data)
        db.commit()
    return {"detail": "操作成功"}


@router.delete("/i/{item_id}", response_model=schemas.Msg)
async def delete_item(
    item_id: str, db: Session = Depends(get_db),
    _: models.Users = Depends(check_admin),
) -> schemas.Msg:
    """通过id删除项目"""
    db.query(models.Items).filter(models.Items.id==item_id).delete()
    db.commit()
    return {"detail": "操作成功"}


@router.get("/t/", response_model=list[schemas.CommentOut])
async def read_talks(
    skip: int = 0, db: Session = Depends(get_db),
    _: models.Users = Depends(check_admin),
) -> list[schemas.CommentOut]:
    """检索所有评论"""
    return db.query(models.Comment).offset(skip*40).limit(40).all()


@router.delete("/t/{talk_id}", response_model=schemas.Msg)
async def delete_talk(
    talk_id: str, db: Session = Depends(get_db),
    _: models.Users = Depends(check_admin),
) -> schemas.Msg:
    """通过id删除评论"""
    db.query(models.Comment).filter(models.Comment.id==talk_id).delete()
    db.commit()
    return {"detail": "操作成功"}
