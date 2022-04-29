from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, ForeignKey

from core.database import Base


class Courier(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(50))
    email = Column(String(100), unique=True, index=True)
    number = Column(String(50))
    address = Column(String(50))
    hashed_password = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_active = Column(Boolean, default=True)


class VerificationCode(Base):
    __tablename__ = "verification_code"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    user = Column(String, ForeignKey("users.email", ondelete='CASCADE'))
    code = Column(Integer, unique=True)
