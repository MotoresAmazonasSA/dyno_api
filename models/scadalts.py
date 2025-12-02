from sqlalchemy import Column, BigInteger, Integer
from sqlalchemy.dialects.mysql import DATETIME, DOUBLE
from database import Base
from datetime import datetime


class LatestTest(Base):
    __tablename__ = "latest_test"
    timestmp = Column(DATETIME(fsp=4), primary_key=True)
    meta_ntc1 = Column(DOUBLE)
    meta_ntc3 = Column(DOUBLE)
    meta_ntc5 = Column(DOUBLE)
    meta_peso_1 = Column(DOUBLE)
    meta_corriente_1 = Column(DOUBLE)
    meta_corriente_2 = Column(DOUBLE)
    meta_ntc2 = Column(DOUBLE)
    meta_ntc6 = Column(DOUBLE)
    meta_lv25p_1 = Column(DOUBLE)
    meta_lv25p_2 = Column(DOUBLE)
    meta_encoder = Column(DOUBLE)
    meta_ntc4 = Column(DOUBLE)
    meta_peso_2 = Column(DOUBLE)


class TestInfo(Base):
    __tablename__ = "test_info"

    test_id = Column(Integer, primary_key=True)
    begin_of_test = Column(BigInteger)
    end_of_test = Column(BigInteger)

    @property
    def inicio_test(self):
        return datetime.fromtimestamp(self.begin_of_test / 1000)

    @property
    def fin_test(self):
        return datetime.fromtimestamp(self.end_of_test / 1000)
