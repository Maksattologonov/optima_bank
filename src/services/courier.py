import random
import smtplib
import sqlalchemy
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from email.message import EmailMessage
from decouple import config
from jinja2 import Template
from starlette.responses import JSONResponse
from passlib.hash import bcrypt, des_crypt
from fastapi import status
from pydantic import ValidationError

from common.message import raw
from core.database import get_session, Session
from core.settings import settings
from datetime import datetime, timedelta
from models import courier
from jose import (
    jwt,
    JWTError
)

from models.courier import Courier, VerificationCode
from schemas.courier import (
    TokenSchema,
    UserSchema, UserCreateSchema
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/courier/sign-in')

conn = Session()


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserSchema:
    return AuthService.validate_token(token)


class AuthService:
    @classmethod
    def get_user(cls, **filters):
        return conn.query(Courier).filter_by(**filters).first()

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def validate_token(cls, token: str) -> UserSchema:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Не удалось валидировать учетные данные',
            headers={
                'WWW-Authenticate': 'Bearer'
            },
        )
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
            )
        except JWTError:
            raise exception
        user_data = payload.get('user')
        try:
            user = UserSchema.parse_obj(user_data)
        except ValidationError:
            raise exception
        return user

    @classmethod
    def create_token(cls, user: Courier) -> TokenSchema:
        user_data = UserSchema.from_orm(user)
        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=settings.jwt_expirations),
            'sub': str(user_data.id),
            'user': user_data.dict(),
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )
        return TokenSchema(access_token=token)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_user(self, user_data: UserCreateSchema):
        exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Повторяющееся значение ключа нарушает уникальное ограничение',
        )
        try:
            user = Courier(
                name=user_data.name,
                email=user_data.email,
                number=user_data.number,
                address=user_data.address,
                hashed_password=self.hash_password(user_data.password),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                is_active=False
            )
            self.session.add(user)
            self.session.commit()
            SendMessageWhenCreateUser.send_email_async(email=user_data.email)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content="Аккаунт успешно зарегистрирован, для использования пройдите верификацию"
            )
        except sqlalchemy.exc.IntegrityError:
            raise exception

    def authenticate_user(self, email: str, password: str) -> TokenSchema:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неправильный адрес электронной почты или пароль',
            headers={
                'WWW-Authenticate': 'Bearer'
            },
        )
        user = (
            self.session
                .query(Courier)
                .filter(Courier.email == email)
                .first()
        )
        if not user:
            raise exception

        if not self.verify_password(password, user.hashed_password):
            raise exception
        return self.create_token(user)

    def refresh_token(self, pk: int) -> TokenSchema:
        user = self.get_user(id=pk)
        if user:
            return self.create_token(user)
        exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                  detail='Пользователь не найден')
        raise exception from None

    @classmethod
    def update_profile(cls, pk: int, name: str, last_name: str, anonymous_name: str):
        query = conn.query(Courier).filter_by(id=pk)
        try:
            if name:
                query.update({"name": name})
                conn.commit()
            if last_name:
                query.update({"last_name": last_name})
                conn.commit()
            if anonymous_name:
                query.update({"anonymous_name": anonymous_name})
                conn.commit()
            return query.first()
        except Exception as ex:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Параметры не могут быть пустыми")

    @classmethod
    def reset_password(cls, email: str, code: int, new_password: str, confirm_password: str):
        if conn.query(Courier).filter_by(email=email).first():
            if conn.query(VerificationCode).filter_by(code=code).first():
                if new_password == confirm_password:
                    table = Courier.__table__
                    stmt = table.update().values(hashed_password=cls.hash_password(new_password))
                    conn.execute(stmt)
                    conn.commit()
                    return HTTPException(status_code=status.HTTP_200_OK,
                                         detail="Пароль успешно изменен")
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Пароли не совпадают")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Неправильный код")
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Запрос не может быть пустым")


class SendMessageWhenCreateUser:
    model = VerificationCode

    @classmethod
    def activate_user(cls, email: str, code: int):
        exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Активационный код был введен некорректно',
        )
        if conn.query(cls.model).filter_by(user=email, code=code).first():
            user = conn.query(Courier).filter_by(email=email).first()
            if not user.is_active:
                user.is_active = True
                conn.commit()
                cls.delete(user=email)
                return AuthService.create_token(user)
        raise exception

    @classmethod
    def check_code(cls, **filters):
        return conn.query(cls.model).filter_by(**filters).all()

    @classmethod
    def delete(cls, **filters):
        conn.query(cls.model).filter_by(**filters).delete()
        conn.commit()

    @classmethod
    def update_code(cls, email: str, code: int):
        conn.query(cls.model).filter_by(user=email).update({"code": code})
        conn.commit()

    @classmethod
    def create_record(cls, user: str, code: int):
        email = AuthService.get_user(email=user)
        query = cls.model(user=user, code=code)
        conn.add(query)
        conn.commit()

    @classmethod
    async def send_email_async(cls, email: str):
        record = conn.query(Courier).filter_by(email=email).first()
        if record:
            bar = Template(raw)
            code = cls.verification_code(email=email)
            template = bar.render(messages={'name': f"{record.name}", 'code': code})
            message = EmailMessage()
            message['Subject'] = f'Здравствуйте {record.name}!'
            message['From'] = config("MAIL_FROM")
            message['To'] = email
            message.add_alternative(template, subtype='html')
            smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp.login(config("MAIL_FROM"), config("MAIL_PASSWORD"))
            smtp.send_message(message)
            smtp.quit()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content="Сообщение успешно отправлено"
            )
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    @staticmethod
    def generate_code() -> int:
        return random.randint(100000, 999999)

    @classmethod
    def verification_code(cls, email: str):
        code = cls.generate_code()
        if not cls.check_code(code=code):
            if cls.check_code(user=email):
                cls.update_code(email=email, code=code)
            else:
                cls.create_record(user=email, code=code)
        return code
