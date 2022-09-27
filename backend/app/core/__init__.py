"""配置参数"""
import os


class Config:

    @staticmethod
    def env(val: str = "") -> str:
        """环境变量获取"""
        return os.getenv(val, "")

    server = {
        # 基础服务器信息
        # "title": "bbs",
        # "version": "0.0.1",

        # API接口文档
        # "doc_url": None,
        # "redoc_url": None,
        # "openapi_url": None,
    }

    connect = {
        # 数据库对接参数
        # "url": f"sqlite:///{__path__[0]}/Server.db",
        # "connect_args": {"check_same_thread": False},
        "url": env("alchemy"),
    }

    emial = {
        # 邮件配置
        "host": env("emailh"),
        "user": env("emailu"),
        "password": env("emailp"),
    }

    security = {
        # 安全配置
        "key": env("key").encode("utf8"),
        "digestmod": env("digestmod") or "sha256",
    }
