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
        Column("ban", Boolean, default=0),
        Column("tag", String(128)),
        Column("body", TEXT(6500)),
        Column("time", Integer, default=lambda: int(time())),
    )
    id: Column
    author: Column
    title: Column
    ban: Column
    tag: Column
    body: Column
    time: Column


class Comment(Base):
    __table__ = Table(
        "Comment",
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


Base.metadata.create_all(engine)
