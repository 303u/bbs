from fastapi import APIRouter, HTTPException, Depends

from ..base import models, schemas
from ..core.dependence import Session, get_db, check_user


router = APIRouter(
    prefix="/t",
    tags=["talks"],
)


@router.get("/{item_id}", response_model=list[schemas.TalkOut])
async def select(
    item_id: str, db: Session = Depends(get_db),
    _: models.Users = Depends(check_user),
) -> list[schemas.TalkOut]:
    """查询评论"""
    return db.query(models.Talks).filter(models.Talks.item == item_id).all()


@router.post("/", response_model=schemas.Msg)
async def insert(
    user_in: schemas.TalksIn, db: Session = Depends(get_db),
    user: models.Users = Depends(check_user),
) -> schemas.Msg:
    """新建评论"""
    talk = db.query(models.Items).filter(models.Items.id==user_in.item)
    if not talk.first():
        raise HTTPException(404, "项目不存在")
    db.add(models.Talks(**user_in.dict(
        exclude_defaults=True), author=user.id))
    db.commit()
    return {"detail": "操作成功"}


@ router.delete("/{talk_id}", response_model=schemas.Msg)
async def delete(
    talk_id: str, db: Session = Depends(get_db),
    user: models.Users = Depends(check_user),
) -> schemas.Msg:
    """通过id删除评论"""
    talk: models.Talks | None = db.query(models.Talks).filter(
        models.Talks.id == talk_id).first()
    if not talk:
        raise HTTPException(404, "项目不存在")
    elif not talk.author == user.id:
        raise HTTPException(403, "权限不足")
    db.delete(talk)
    db.commit()
    return {"detail": "操作成功"}
