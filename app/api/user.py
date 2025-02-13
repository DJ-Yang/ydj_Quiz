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


@router.post("/login", response_model=ResponseUser)
@inject
async def login(
nickname: Annotated[str, Form(description="닉네임", example="닉네임")],
    password: Annotated[str, Form(description="비밀번호", example="비밀번호")],
    current_user: currentUser,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    # eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMiJ9.-HSiApoYzM87wa8-mRPxZs0vwNjQBCVMLTmROOD5-1A
    return ResponseUser(
        code=status.HTTP_200_OK,
        message="사용자 조회를 완료했습니다.",
        data=await user_service.get_user(current_user),
    )


