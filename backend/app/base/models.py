from time import time
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy import Boolean, TEXT,  Integer
from sqlalchemy.orm import relationship

from . import Base, engine


class User(Base):
    __tablename__ = "user"
    id = Column("id", Integer, primary_key=1, index=1)
    # 账号基础信息
    email = Column("email", String(64), unique=1, index=1)
    password = Column("password", String(24), nullable=False)
    # 用户身份与状态
    active = Column("active", Boolean, default=1)
    admin = Column("admin", Boolean, default=0)
    # 反向绑定用户信息
    info: "Info" = relationship("Info", uselist=False)


class Info(Base):
    __tablename__ = "info"
    id = Column("id", ForeignKey("user.id"), primary_key=1, index=1)
    # 主要信息
    name = Column("name", String(20), default=id, nullable=False)
    motto = Column("motto", String(50))
    phone = Column("phone", String(20))
    # 相关信息
    gender = Column("gender", Boolean, default=1)
    city = Column("city", String(20))
    hobby = Column("hobby", String(20))
    birthday = Column("birthday", Integer, default=0)
    # 状态
    last_login = Column("last_login", Integer, default=lambda: int(time()))
    item_count = Column("item_count", Integer, default=0)


class Item(Base):
    __tablename__ = "item"
    id = Column("id", Integer, primary_key=1, index=1)
    # 内容
    author = Column("author", ForeignKey("user.id"), nullable=False)
    title = Column("title", String(64), index=1)
    tag = Column("tag", String(128))
    description = Column("description", String(200))
    content = Column("content", TEXT)
    # 状态
    ban = Column("ban", Boolean, default=0)
    hits = Column("hits", Integer, default=0)
    time = Column("time", Integer, default=lambda: int(time()))


class Comment(Base):
    __tablename__ = "comment"
    id = Column("id", Integer, primary_key=1, index=1)
    # 关联
    item = Column("item", ForeignKey(
        "item.id", ondelete="CASCADE"), nullable=False, index=1)
    author = Column("author", ForeignKey("info.id"), nullable=False)
    reply = Column("reply", ForeignKey("info.id", ondelete="SET NULL"))
    # 数据
    body = Column("body", String(300), nullable=False)
    time = Column("time", Integer, default=lambda: int(time()))


class Banner(Base):
    __tablename__ = "banner"
    id = Column("id", Integer, primary_key=1)
    # 链接
    url = Column("url", String(120))
    img = Column("img", String(120))
    # 信息
    title = Column("title", String(20))
    description = Column("description", String(300))
    # 状态
    start = Column("start", Integer, default=lambda: int(time()))
    end = Column("end", Integer, default=0)
    hits = Column("hits", Integer, default=0)


Base.metadata.create_all(engine)
