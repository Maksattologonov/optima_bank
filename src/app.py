from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from apis.courier import router as courier_router

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
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


app = get_application()
