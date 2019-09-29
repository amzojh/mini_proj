import inspect
from abc import ABCMeta
from sqlalchemy import Column, Integer, String, ForeignKey, Float, TIMESTAMP

try:
    from database import Base
except:
    from Database import Base


class baseAbstract(Base):
    __abstract__ = True

    def __init__(self):
        pass

    def __repr__(self):
        return f"""
            table name : {self.__tablename__} 
        """

class dartReportType(baseAbstract):
    __tablename__ = "DartReportType"
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(30), unique=True)
    company_name = Column(String(60))
    sector = Column(String(30))
    industry = Column(String(60))
    market = Column(String(20))

# DB Table

class dartReportList(baseAbstract):
    __tablename__ = "DartReportList"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol= Column(String(30))
    issue_company = Column(String(60))
    issue_date = Column(String(10))
    report_link = Column(String(200))
    report_name = Column(String(60))
    disclosure_company = Column(String(60))
    report_id = Column(String(13), unique=True)


# class dartReportList(baseAbstract):
#     __tablename__ = "DartReportList"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     symbol= Column(String(30))
#     issue_company = Column(String(60))
#     issue_date = Column(String(10))
#     report_link = Column(String(200))
#     report_name = Column(String(60))
#     disclosure_company = Column(String(60))
#     report_id = Column(String(13), unique=True)