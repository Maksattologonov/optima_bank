from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, ForeignKey

from core.database import Base


class Bid(Base):
    __tablename__ = "bid"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    city = Column(String(100), nullable=False)
    code = Column(Integer, unique=True, nullable=False)
    address_delivery = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=False)
    number = Column(String(50), nullable=False)
    address_live = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    image_1 = Column(String(255), nullable=False)
    image_2 = Column(String(255), nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime)
    status = Column(String(50), nullable=False)
