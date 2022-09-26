"""数据对接"""

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from ..core import Config

# 模型
Base = declarative_base()
# 引擎
engine = sqlalchemy.create_engine(**Config.connect)
# 会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
