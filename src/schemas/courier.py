from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel, validator


class CreateCourierSchema(BaseModel):
    name: str
    last_name: str
    email: str
    password: str


class UserSchema(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class UserCreateSchema(BaseModel):
    name: str
    email: str
    number: str
    address: str
    password: str

    class Config:
        orm_mode = True

    @validator('password')
    def validate_password(cls, v):
        if len(v) > 8:
            return v
        raise ValueError("Пароль должен быть более 8 символов")


class UserGetSchema(BaseModel):
    id: Optional[int]
    email: Optional[str]
    name: Optional[str]
    address: Optional[str]
    number: Optional[str]

    class Config:
        orm_mode = True


class EmailSchema(BaseModel):
    email: str

    class Config:
        orm_mode = True


class VerifiedCodeSchema(BaseModel):
    email: str
    code: int

    @validator("code")
    def validate_code(cls, v):
        exception = HTTPException(
            status_code=status.HTTP_411_LENGTH_REQUIRED,
            detail='Код активации должен состоять из 6 цифр',
        )
        if len(str(v)) == 6:
            return v
        raise exception
