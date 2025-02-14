from typing import Annotated
from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject
from fastapi.security import HTTPBearer
from starlette import status

from app.containers import Container

from app.service.auth import AuthService


oauth2_scheme = HTTPBearer()
router = APIRouter(tags=["user"])
currentUser = Annotated[str, Depends(AuthService.get_current_user)]



