from pydantic import BaseModel, Field


class Token(BaseModel):
    """返回身份令牌"""
    access_token: str = None


class Msg(BaseModel):
    """返回响应信息"""
    detail: str = None


class VerifyCode(Msg):
    """返回验证信息"""
    token: str = None


# 用户系列
class UserIn(BaseModel):
    """用户模型输入"""
    name: str = Field(None, min_length=1, max_length=20)
    email: str = Field(None, regex=r"\w{2,32}\@\w+\.\w+", max_length=64)
    password: str = Field(None, min_length=6, max_length=24)


class UserOut(BaseModel):
    """用户模型输出"""
    id: str = None
    name: str = None

    class Config:
        orm_mode = True


class UserFull(UserOut):
    """用户最终模型"""
    info: str = None
    email: str = None
    admin: bool = None
    active: bool = None
    password: str = None


# 数据系列
class ItemIn(BaseModel):
    """用户项目输入"""
    title: str = Field(..., min_length=1, max_length=32)
    tag: str = Field(None, max_length=128)
    body: str = Field(None, max_length=6500)


class ItemOut(BaseModel):
    """用户项目输出"""
    id: str = None
    author: str = None
    title: str = None
    tag: str = None
    body: str = None
    time: str = None

    class Config:
        orm_mode = True


class ItemFull(ItemOut):
    """项目最终模型"""
    ban: bool = None


# 评论系列
class TalksIn(BaseModel):
    """评论模型输入"""
    body: str = Field(..., min_length=1, max_length=300)
    item: str = Field(..., min_length=16, max_length=16)
    reply: str = Field(None, max_length=16)


class TalkOut(BaseModel):
    """评论模型输出"""
    id: str = None
    item: str = None
    author: str = None
    reply: str = None
    body: str = None
    time: str = None

    class Config:
        orm_mode = True
