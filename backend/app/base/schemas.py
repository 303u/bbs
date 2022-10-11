from pydantic import BaseModel, Field


class Token(BaseModel):
    """返回身份令牌"""
    access_token: str = None


class Msg(BaseModel):
    """返回响应信息"""
    detail: str = "done"


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
    title: str = Field(..., min_length=1, max_length=64)
    tag: str = Field(None, max_length=128)
    content: str = Field(None, max_length=6500)
    description: str = Field(None, max_length=200)


class ItemOut(BaseModel):
    """用户项目输出"""
    id: str = None
    author: str = None
    title: str = None
    time: str = None
    tag: str = None
    description: str = None
    hits: int = None

    class Config:
        orm_mode = True


class ItemFullOut(ItemOut):
    """用户项目内容"""
    content: str = None


class ItemFull(ItemFullOut):
    """项目最终模型"""
    ban: bool = None


# 用户详细信息
class InfoIn(BaseModel):
    """用户详细信息输入"""
    gender: bool = None
    city: str = None
    hobby: str = None
    birthday: int = None
    motto: str = None


class InfoOut(InfoIn):
    """用户详细信息输出"""
    last_login: int = None
    item_count: int = None

    class Config:
        orm_mode = True


# 评论系列
class CommentIn(BaseModel):
    """评论模型输入"""
    body: str = Field(..., min_length=1, max_length=300)
    item: str = Field(..., min_length=16, max_length=16)
    reply: str = Field(None, max_length=16)


class CommentOut(BaseModel):
    """评论模型输出"""
    id: str = None
    item: str = None
    author: str = None
    reply: str = None
    body: str = None
    time: str = None

    class Config:
        orm_mode = True


# 推广项目
class Banner(BaseModel):
    """推广项目模型"""
    url: str = None
    img: str = None
    title: str = None
    start: int = None
    end: int = None
    hits: int = None
    description: str = None

    class Config:
        orm_mode = True
