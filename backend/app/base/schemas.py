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
    id: int = None

    class Config:
        orm_mode = True


class UserFull(UserOut):
    """用户最终模型"""
    info: str = None
    email: str = None
    password: str = None
    active: bool = None
    admin: bool = None


# 用户详细信息
class InfoIn(BaseModel):
    """用户详细信息输入"""
    name: str = None
    motto: str = None
    phone: str = None

    gender: bool = None
    city: str = None
    hobby: str = None
    birthday: int = None


class InfoOut(InfoIn):
    """用户详细信息输出"""
    id: int = None
    phone: bool = None

    last_login: int = None
    item_count: int = None

    class Config:
        orm_mode = True


# 数据系列
class ItemIn(BaseModel):
    """用户项目输入"""
    title: str = Field(..., min_length=1, max_length=64)
    tag: str = Field(None, max_length=128)
    description: str = Field(None, max_length=200)
    content: str = Field(None, min_length=1)


class ItemOut(BaseModel):
    """用户项目输出"""
    id: int = None

    author: str = None
    title: str = None
    tag: str = None
    description: str = None

    hits: int = None
    time: str = None

    class Config:
        orm_mode = True


class ItemFull(ItemOut):
    """项目最终模型"""
    content: str = None
    ban: bool = None


# 真正读取content内容的项目模型
class ContentOut(ItemOut):
    """用户项目内容"""
    content: str = None


# 评论系列
class CommentIn(BaseModel):
    """评论模型输入"""
    item: int = Field(...)
    reply: int = Field(0)
    body: str = Field(..., max_length=300)


class CommentOut(BaseModel):
    """评论模型输出"""
    id: int = None

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
    description: str = None

    start: int = None
    end: int = None
    hits: int = None

    class Config:
        orm_mode = True
