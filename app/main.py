import os
import json
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import logging.config

from fastapi import FastAPI, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.containers import Container
from app.service.auth import AuthService
from app.middleware.request import base_http_middleware

from app.api import user, auth, quiz

container = Container()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
)


app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=base_http_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

app.container = container
app.include_router(auth.router, prefix="/api/user")
app.include_router(user.router, prefix="/api/user", dependencies=[Depends(AuthService.get_current_user)])
app.include_router(quiz.router, prefix="/api/quiz", dependencies=[Depends(AuthService.get_current_user)])

def setup_logging():
    current_dir = os.path.dirname(os.path.realpath(__file__))  # 현재 파일의 디렉토리 절대 경로
    config_path = os.path.join(current_dir, 'logging.json')  # 로깅 설정 파일의 절대 경로

    if os.path.exists(config_path):
        with open(config_path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        print(f"Cannot find logging configuration file at {config_path}")

@app.get(
    "/health",
    responses={
        200: {
            "description": "Server Alive",
            "content": {
                "application/json": {
                    "example": {
                        "status": "alive",
                    },
                }
            },
        },
        422: {"description": "Validation Error"},
    },
    status_code=status.HTTP_200_OK,
    description="Health Check API",
    summary="Health Check",
)
async def health_check() -> dict[str, str]:
    return {"status": "alive"}

if __name__=='__main__':
    uvicorn.run('0.0.0.0', port=10011)