from sqlalchemy import Column, Integer, String, ForeignKey, Float, TIMESTAMP

try:
    from database import Base
except:
    from Database import Base


class baseAbstract(Base):
    __abstract__ = True
    def __repr__(self):
        return f"""
            table name : {self.__tablename__} 
        """
    


class dartReportType(baseAbstract):
    __tablename__ = "DartReportType"
    symbol = Column(String(30), nullable=False)
    company_name = Column(String(60), nullable=False)
    sector = Column(String(30))
    industry = Column(String(60))
    market = Column(String(20))

class dartReportList(baseAbstract):
    __tablename__ = "DartReportList"
