from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, ForeignKey

from core.database import Base


class District(Base):
    __tablename__ = "districts"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    districts = Column(String, unique=True, nullable=False)
