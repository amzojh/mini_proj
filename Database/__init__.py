from types import MethodType

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session

from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import ClauseElement

try:
    from .settings import config
except:
    from settings import config

engine = create_engine(config, convert_unicode=True)

# 동적 class를 생성
Session = sessionmaker(bind=engine)

Base = declarative_base()

db_session = scoped_session(Session)
Base.query = db_session.query_property()
Base.metadata.create_all(engine)