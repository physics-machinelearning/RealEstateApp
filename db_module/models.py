from sqlalchemy import create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column, UniqueConstraint
from sqlalchemy.types import Integer, String, Text, Float, Boolean
from datetime import datetime

Base = declarative_base()


class RentProperty(Base):
    __tablename__ = 'rentproperty'
    __table_args__ = (UniqueConstraint('url'), {})

    # id
    property_id = Column(Integer, primary_key=True, autoincrement=True)

    # 登録日
    date = Column(DateTime, default=datetime.now)

    # 賃料
    rent = Column(Float)

    # 管理費
    kanrihi = Column(Float)

    #　敷金
    sikikin = Column(Float)

    #　礼金
    reikin = Column(Float)

    # アパート名
    subtitle = Column(String(50))

    # 住所
    location = Column(String(50))

    # 経度
    latitude = Column(Float)

    # 緯度
    longititude = Column(Float)

    # 一番近い駅まで徒歩でかかる時間（分）
    close_station = Column(Integer)

    # 間取り
    floor_plan = Column(String(50))

    # 面積
    area = Column(Float)

    # 築年数
    age = Column(Float)

    # 階数
    floor = Column(Integer)

    #　向き
    orientation = Column(String(5))

    #　バストイレ別
    bath_toilet = Column(Boolean)

    # オートロック
    auto_lock = Column(Boolean)

    # 情報が掲載されているurl
    url = Column(String(1000), primary_key=True)

    predicted_rent = Column(Float)

    rent_diff = Column(Float)


class AddressCoordinate(Base):
    __tablename__ = 'coordinate'

    address = Column(String(100), primary_key=True)

    latitude = Column(Float)

    longititude = Column(Float)


if __name__ == '__main__':
    engine = create_engine("postgresql://kuroki:kuroki@localhost:5432/suumo-db")
    Base.metadata.create_all(engine)
    # Base．metadata drop＿all(engine)
