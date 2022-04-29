from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from apis.courier import router as courier_router
from apis.bid import router as bid_router
from images.media import router as media_router

templates = Jinja2Templates(directory='common/templates')

origins = [
    "http://localhost:3000",
    "https://localhost:8000",
    "http://localhost:8000",
    "http://localhost:8080",
]


def get_application() -> FastAPI:
    application = FastAPI(
        title='Account',
        description='Psychology therapy',
        version='1.0.0',
    )
    application.include_router(router=courier_router)
    application.include_router(router=bid_router)
    application.include_router(router=media_router)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


app = get_application()
