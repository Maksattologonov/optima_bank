from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from core.database import Session, get_session
from schemas.courier import CreateCourierSchema, UserCreateSchema, TokenSchema, UserGetSchema, UserSchema, EmailSchema, \
    VerifiedCodeSchema
from services.courier import AuthService, get_current_user, SendMessageWhenCreateUser

router = APIRouter(
    prefix='/courier',
    include_in_schema=True,
    tags=['courier']
)


@router.post('/sign-up', response_model=TokenSchema)
def sign_up(
        user_data: UserCreateSchema,
        service: AuthService = Depends()
):
    return service.register_user(user_data)


@router.post('/sign-in', response_model=TokenSchema)
def sign_in(
        form_data: OAuth2PasswordRequestForm = Depends(),
        service: AuthService = Depends()
):
    return service.authenticate_user(form_data.username, form_data.password)


@router.get('/user', response_model=UserGetSchema)
def get_user(user: UserSchema = Depends(get_current_user)):
    return AuthService.get_user(id=user.id)


@router.post('/send-email')
async def send_email_asynchronous(response_model: EmailSchema):
    return await SendMessageWhenCreateUser.send_email_async(email=response_model.email)


@router.post('/verified-account', response_model=TokenSchema)
def verified_account(form_data: VerifiedCodeSchema, service: SendMessageWhenCreateUser = Depends()):
    return service.activate_user(email=form_data.email, code=form_data.code)


@router.get("/get-delivery")
def get_delivery(user: UserSchema = Depends(get_current_user),
                 db: Session = Depends(get_session),
                 ):
    return SendMessageWhenCreateUser.get_delivery(db=db, user_id=user.id)
