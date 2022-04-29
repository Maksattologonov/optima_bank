from fastapi import APIRouter, Depends, UploadFile, File, status

from core.database import Session, get_session
from schemas.bid import CreateBidSchema
from services.bid import BidService

router = APIRouter(
    prefix='/bid',
    include_in_schema=True,
    tags=['bid']
)


@router.post("/create")
def create_bid(
        form: CreateBidSchema = Depends(),
        db: Session = Depends(get_session),
        image_1: UploadFile = File(...),
        image_2: UploadFile = File(...),
        service: BidService = Depends()
):
    return service.create(bid_form=form, db=db, image_1=image_1, image_2=image_2)


@router.get("/get")
def get_bid(
        email: str,
        db: Session = Depends(get_session),
        service: BidService = Depends()
):
    return service.get(db=db, email=email)
