"""路径路由"""

from fastapi import APIRouter

from . import login
from . import users
from . import items
from . import info
from . import intro
from . import comment
from . import admin


class Router(APIRouter):

    def __init__(self, url_path: str = "") -> None:
        super().__init__(prefix=url_path)
        self.include_router(login.router)
        self.include_router(users.router)
        self.include_router(items.router)
        self.include_router(info.router)
        self.include_router(intro.router)
        self.include_router(comment.router)
        self.include_router(admin.router)
