from pydantic import BaseModel


class CreateBidSchema(BaseModel):
    city: str
    address_delivery: str
    name: str
    last_name: str
    middle_name: str
    number: str
    address_live: str
    district: str
    email: str
    comment: str


class GetBidSchema(BaseModel):
    city: str
    address_delivery: str
    name: str
    last_name: str
    middle_name: str
    number: str
    address_live: str
    email: str
    district: str
    comment: str
