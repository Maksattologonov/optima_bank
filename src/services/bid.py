import random
from datetime import datetime

import sqlalchemy
from fastapi import HTTPException, status, UploadFile
from starlette.responses import JSONResponse

from core.database import Session
from models.bid import Bid
from schemas.bid import CreateBidSchema


class BidService:
    model = Bid

    @classmethod
    def create(cls, db: Session, bid_form: CreateBidSchema, image_1: UploadFile, image_2: UploadFile):
        exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Повторяющееся значение нарушает уникальное ограничение',
        )
        try:
            img_1 = cls.save_image(image=image_1)
            img_2 = cls.save_image(image=image_2)
            code = cls.generate_code()
            user = Bid(
                name=bid_form.name,
                last_name=bid_form.last_name,
                middle_name=bid_form.middle_name,
                email=bid_form.email,
                number=bid_form.number,
                address_delivery=bid_form.address_delivery,
                address_live=bid_form.address_live,
                code=code,
                city=bid_form.city,
                image_1=img_1,
                image_2=img_2,
                comment=bid_form.comment,
                status='Заявка создана',
                created_at=datetime.utcnow(),
            )
            db.add(user)
            db.commit()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content="Заявка создана, ждите звонка"
            )
        except sqlalchemy.exc.IntegrityError:
            raise exception

    @staticmethod
    def save_image(image: UploadFile):
        if image:
            url = f'images/{image.filename}'
            with open(url, 'wb') as file:
                file.write(image.file.read())
                file.close()
                return url
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Изображение не может быть пустым")

    @classmethod
    def get(cls, db: Session, **filters):
        query = db.query(cls.model).filter_by(**filters).first()
        if query:
            return query
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Заявка не найдена")

    @staticmethod
    def generate_code() -> int:
        return random.randint(10000000, 99999999)

    @classmethod
    def update_code(cls, db: Session, email: str, code: int):
        db.query(cls.model).filter_by(user=email).update({"code": code})
        db.commit()

    @classmethod
    def create_code(cls, db: Session,  email: str):
        return cls.generate_code()
