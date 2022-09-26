"""项目入口"""

from fastapi import FastAPI

from .core import *
from .path import *

# 启动程序
app = FastAPI(**Config.server)
app.include_router(Router(""))
