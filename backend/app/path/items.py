from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import or_, and_

from ..base import models, schemas
from ..core.dependence import Session, get_db, check_user, check_item


router = APIRouter(
    prefix="/i",
    tags=["items"],
)


@router.get("/", response_model=list[schemas.ItemOut])
async def get_items(
    o: int = 0, me: bool = False,
    db: Session = Depends(get_db),
    user: models.Users = Depends(check_user),
) -> list[schemas.ItemOut]:
    """获取项目内容"""
    items = db.query(models.Items).filter(models.Items.ban == False)
    if me:
        items = items.filter(models.Items.author == user.id)
    else:
        items = items.filter(models.Items.author != user.id)
    return items.offset(o*40).limit(40).all()


@router.get("/{item_id}", response_model=schemas.ItemOut)
async def get_item(
    item_id: str, db: Session = Depends(get_db),
    _: models.Users = Depends(check_user),
) -> schemas.ItemOut:
    """获取项目内容"""
    items = db.query(models.Items).filter(
        models.Items.id == item_id, models.Items.ban == False).first()
    if items:
        return items
    else:
        raise HTTPException(404, "项目不存在")


@router.post("/", response_model=schemas.Msg)
async def create_item(
    data: schemas.ItemIn,
    db: Session = Depends(get_db),
    user: models.Users = Depends(check_user),
) -> schemas.Msg:
    """创建数据内容"""
    db.add(models.Items(**data.dict(), author=user.id))
    db.commit()
    return {"detail": "操作成功"}


@router.put("/{item_id}", response_model=schemas.Msg)
async def update_item(
    data: schemas.ItemIn,
    db: Session = Depends(get_db),
    user: models.Users = Depends(check_user),
    item: models.Items = Depends(check_item),
) -> schemas.Msg:
    """通过id更新内容"""
    if item.author != user.id:
        raise HTTPException(400, "权限不足")
    elif not (update_data := data.dict(exclude_defaults=True)):
        user.active = False
        db.commit()
        raise HTTPException(415, "恶意提交数据")
    db.query(models.Items).filter(
        models.Items.id == item.id).update(update_data)
    db.commit()
    return {"detail": "操作成功"}


@router.delete("/{item_id}", response_model=schemas.Msg)
async def delete_item(
    db: Session = Depends(get_db),
    user: models.Users = Depends(check_user),
    item: models.Items = Depends(check_item),
) -> schemas.Msg:
    """通过id删除项目"""
    if item.author != user.id:
        raise HTTPException(400, "权限不足")
    db.query(models.Talks).filter(models.Talks.item == item.id).delete()
    db.delete(item)
    db.commit()
    return {"detail": "操作成功"}


@router.get("/t/{key_words}", response_model=list[schemas.ItemOut])
async def take_item(
    key_words: str, o: int = 0,
    db: Session = Depends(get_db),
    _: models.Users = Depends(check_user),
) -> list[schemas.ItemOut]:
    """获取关键字内容"""
    title = [models.Items.title.like(f"%{w}%") for w in key_words.split(" ")]
    tag = [models.Items.tag.like(f"%{w}%") for w in key_words.split(" ")]
    return db.query(models.Items).filter(models.Items.ban == False).filter(
        or_(and_(*title), and_(*tag))).offset(o*40).limit(40).all()
