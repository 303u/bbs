"""路径路由"""

from fastapi import APIRouter

from . import login
from . import users
from . import items
from . import admin
from . import talks


class Router(APIRouter):

    def __init__(self, url_path: str = "") -> None:
        super().__init__(prefix=url_path)
        self.include_router(login.router)
        self.include_router(users.router)
        self.include_router(items.router)
        self.include_router(admin.router)
        self.include_router(talks.router)
