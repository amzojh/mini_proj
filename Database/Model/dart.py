import inspect
from abc import ABCMeta
from sqlalchemy import Column, Integer, String, ForeignKey, Float, TIMESTAMP

try:
    from __init__ import Base
except:
    from Database import Base


__all__ = ["dartReportType", "dartReportList", "dartCompanyList"]

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
    issue_company_id = Column(String(8))
    issue_company = Column(String(60))
    issue_date = Column(String(10))
    report_link = Column(String(200))
    report_name = Column(String(60))
    disclosure_company = Column(String(60))
    report_id = Column(String(13), unique=True)

class dartCompanyList(baseAbstract):
    __tablename__ = "DartCompanyList"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_korean_name = Column(String(255))
    company_english_name = Column(String(255))
    company_name = Column(String(255))
    market_ticker = Column(String(6))
    CEO = Column(String(50))
    company_type = Column(String(30))
    company_registration_number = Column(String(20))
    business_registration_number = Column(String(20))
    address = Column(String(255))
    homepage = Column(String(255))
    ir_url = Column(String(255))
    phone_number = Column(String(30))
    fax = Column(String(30))
    business_type = Column(String(30))
    foundation_date = Column(String(30))
    settlement_month = Column(String(30))
    company_id = Column(String(8), unique=True)
    



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