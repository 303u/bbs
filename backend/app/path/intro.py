from fastapi import APIRouter, Depends

from ..base import models, schemas
from ..core.dependence import Session, get_db, check_user


router = APIRouter(
    prefix="/intro",
    tags=["intro"],
)


@router.get("/banner", response_model=list[schemas.Banner])
async def intro_banner(
    db: Session = Depends(get_db),
    _: models.Users = Depends(check_user),
) -> list[schemas.Banner]:
    """获取推广信息"""
    return db.query(models.Banner).all()


@router.get("/banner/{start}")
async def banner_hits(
    start: int,
    db: Session = Depends(get_db),
    _: models.Users = Depends(check_user),
) -> None:
    """推广栏统计"""
    banner: models.Banner = db.query(models.Banner).filter(
        models.Banner.start == start).first()
    if banner:
        banner.hits += 1
        db.commit()
    return {}


@router.get("/tag", response_model=list[str])
async def intro_tag(
    db: Session = Depends(get_db),
    _: models.Users = Depends(check_user),
) -> list[str]:
    """获取推广标签"""
    return []


@router.get("/user", response_model=list[schemas.UserOut])
async def intro_user(
    db: Session = Depends(get_db),
    _: models.Users = Depends(check_user),
) -> list[schemas.UserOut]:
    """获取推广用户"""
    return db.query(models.Users).limit(12).all()
