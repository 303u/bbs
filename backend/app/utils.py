import yagmail
from fastapi import HTTPException
from yagmail.error import (
    YagAddressError,
    YagConnectionClosed,
    YagInvalidEmailAddress,
)

from .core import Config


def mail_engine(email: str, sub: str, con: str) -> None:
    """邮件发送"""
    try:
        sender = yagmail.SMTP(**Config.emial)
        sender.send(email, sub, con)
    except YagConnectionClosed:
        raise HTTPException(500, "链接被销毁")
    except (YagAddressError, YagInvalidEmailAddress):
        raise HTTPException(400, "无法识别的电子邮件")
    finally:
        sender.close()


def get_code_email(email: str, code: str) -> None:
    """邮箱获取验证码"""
    mail_engine(email, "验证码", code)


def new_account(email: str, name: str) -> None:
    """创建新账号通知"""
    mail_engine(email, "注册成功", name + ": 欢迎加入")


def recovery_code(email: str, code: str) -> None:
    """找回账号通知"""
    mail_engine(email, "验证码", code)


def recovery_success(email: str) -> None:
    """修改密码成功通知"""
    mail_engine(email, "操作成功", "已成功重设密码")
