from core.database import Base
from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, ForeignKey


class Delivery(Base):
    __tablename__ = "delivery"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    courier = Column(Integer, ForeignKey("users.id"), nullable=False)
    bid = Column(Integer, ForeignKey("bid.id"), nullable=False)
    status = Column(String(50), nullable=False, default="Создание заявки")

