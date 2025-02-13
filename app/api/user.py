from typing import Annotated
from fastapi import APIRouter, Body, Depends, Form
from dependency_injector.wiring import Provide, inject
from fastapi.security import HTTPBearer
from starlette import status

from app.containers import Container

from app.service.auth import AuthService
from app.service.user import UserService
from app.schemas.user import ResponseUser


oauth2_scheme = HTTPBearer()
router = APIRouter(tags=["user"])
currentUser = Annotated[str, Depends(AuthService.get_current_user)]



