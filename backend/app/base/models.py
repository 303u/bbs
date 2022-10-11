from time import time
from secrets import token_hex
from sqlalchemy import Table, Column, String, Boolean, TEXT, CHAR, Integer

from . import Base, engine


def create_id() -> str: return f"{int(time())}{token_hex(3)}"


class Users(Base):
    __table__ = Table(
        "users",
        Base.metadata,
        Column("id", CHAR(16), primary_key=1, index=1, default=create_id),
        Column("name", String(20), nullable=0),
        Column("email", String(64), unique=1, index=1),
        Column("password", String(24), nullable=0),
        Column("active", Boolean, default=1),
        Column("admin", Boolean, default=0),
        Column("info", String(16)),
    )
    id: Column
    name: Column
    email: Column
    password: Column
    active: Column
    admin: Column
    info: Column


class Items(Base):
    __table__ = Table(
        "item",
        Base.metadata,
        Column("id", CHAR(16), primary_key=1, index=1, default=create_id),
        Column("author", CHAR(16), nullable=0),
        Column("title", String(64), index=1),
        Column("time", Integer, default=lambda: int(time())),
        Column("ban", Boolean, default=0),
        Column("tag", String(128)),
        Column("description", String(200)),
        Column("content", TEXT(6500)),
        Column("hits", Integer, default=0),
    )
    id: Column
    author: Column
    title: Column
    time: Column
    ban: Column
    tag: Column
    description: Column
    content: Column
    hits: Column


class Info(Base):
    __table__ = Table(
        "info",
        Base.metadata,
        Column("id", CHAR(16), primary_key=1, index=1, default=create_id),
        Column("gender", Boolean, default=1),
        Column("city", String(20)),
        Column("phone", String(20)),
        Column("hobby", String(20)),
        Column("birthday", Integer, default=0),
        Column("motto", String(30)),
        Column("last_login", Integer, default=lambda: int(time())),
        Column("item_count", Integer, default=0),
    )
    id: Column
    gender: Column
    city: Column
    phone: Column
    hobby: Column
    phone: Column
    birthday: Column
    motto: Column
    last_login: Column
    item_count: Column


class Comment(Base):
    __table__ = Table(
        "comment",
        Base.metadata,
        Column("id", CHAR(16), primary_key=1, index=1, default=create_id),
        Column("item", CHAR(16), nullable=0, index=1),
        Column("author", CHAR(16), nullable=0, index=1),
        Column("reply", String(16)),
        Column("body", String(300), nullable=0),
        Column("time", Integer, default=lambda: int(time())),
    )
    id: Column
    item: Column
    author: Column
    reply: Column
    body: Column
    time: Column


class Banner(Base):
    __table__ = Table(
        "banner",
        Base.metadata,
        Column("id", Integer, primary_key=1),
        Column("url", String(120), nullable=0),
        Column("img", String(120)),
        Column("title", String(20)),
        Column("start", Integer, default=lambda: int(time())),
        Column("end", Integer, default=0),
        Column("hits", Integer, default=0),
        Column("description", String(300)),
    )
    id: Column
    url: Column
    img: Column
    title: Column
    start: Column
    end: Column
    hits: Column
    description: Column


Base.metadata.create_all(engine)
