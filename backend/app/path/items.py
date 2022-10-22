from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import or_, and_

from ..base import models, schemas
from ..core.dependence import Session, get_db, check_user, check_item


router = APIRouter(
    prefix="/items",
    tags=["items"],
)


@router.get("/", response_model=list[schemas.ItemOut])
async def get_items(
    skip: int = 0, author: str = "",
    db: Session = Depends(get_db),
    user: models.User = Depends(check_user),
) -> list[schemas.ItemOut]:
    """获取项目内容"""
    items = db.query(models.Item).filter(models.Item.ban == False)
    if author:
        items = items.filter(models.Item.author == author)
    else:
        items = items.filter(models.Item.author != user.id)
    return items.offset(skip*40).limit(40).all()


@router.get("/{item_id}", response_model=schemas.ContentOut)
async def get_item(
    item_id: str, db: Session = Depends(get_db),
    _: models.User = Depends(check_user),
) -> schemas.ContentOut:
    """获取项目内容"""
    items: models.Item = db.query(models.Item).filter(
        models.Item.id == item_id, models.Item.ban == False).first()
    if items:
        items.hits += 1
        db.commit()
        return items
    else:
        raise HTTPException(404, "项目不存在")


@router.post("/", response_model=schemas.Msg)
async def create_item(
    data: schemas.ItemIn,
    db: Session = Depends(get_db),
    user: models.User = Depends(check_user),
) -> schemas.Msg:
    """创建数据内容"""
    db.add(models.Item(**data.dict(), author=user.id))
    # 增加计数
    info: models.Info = db.query(models.Info).filter(
        models.Info.id == user.id).first()
    info.item_count += 1
    db.commit()
    return {}


@router.put("/{item_id}", response_model=schemas.Msg)
async def update_item(
    data: schemas.ItemIn,
    db: Session = Depends(get_db),
    user: models.User = Depends(check_user),
    item: models.Item = Depends(check_item),
) -> schemas.Msg:
    """通过id更新内容"""
    if item.author != user.id:
        raise HTTPException(400, "权限不足")
    elif not (update_data := data.dict(exclude_defaults=True)):
        user.active = False
        db.commit()
        raise HTTPException(415, "恶意提交数据")
    db.query(models.Item).filter(
        models.Item.id == item.id).update(update_data)
    db.commit()
    return {}


@router.delete("/{item_id}", response_model=schemas.Msg)
async def delete_item(
    db: Session = Depends(get_db),
    user: models.User = Depends(check_user),
    item: models.Item = Depends(check_item),
) -> schemas.Msg:
    """通过id删除项目"""
    if item.author != user.id:
        raise HTTPException(400, "权限不足")
    db.query(models.Comment).filter(models.Comment.item == item.id).delete()
    db.delete(item)
    info: models.Info = db.query(models.Info).filter(
        models.Info.id == user.id).first()
    info.item_count -= 1
    db.commit()
    return {}


@router.get("/k/{key_words}", response_model=list[schemas.ItemOut])
async def search_item(
    key_words: str, skip: int = 0,
    db: Session = Depends(get_db),
    _: models.User = Depends(check_user),
) -> list[schemas.ItemOut]:
    """获取关键字内容"""
    title = [models.Item.title.like(f"%{w}%") for w in key_words.split(" ")]
    tag = [models.Item.tag.like(f"%{w}%") for w in key_words.split(" ")]
    return db.query(models.Item).filter(models.Item.ban == False).filter(
        or_(and_(*title), and_(*tag))).offset(skip*40).limit(40).all()
