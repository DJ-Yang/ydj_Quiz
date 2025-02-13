from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Form
from dependency_injector.wiring import Provide, inject
from starlette import status

from app.containers import Container
from app.schemas.user import (
    RequestRegisterDto,
    ResponseRegister,
    ResponseValidate,
    ValidateNickname,
    ResponseUser,
)
from app.service.user import UserService

router = APIRouter(tags=["user"])


@router.post("/validate-nickname", response_model=ResponseValidate)
@inject
async def validate_nickname(
    data: ValidateNickname,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    return ResponseValidate(
        code=status.HTTP_200_OK,
        message="닉네임 중복 검사를 완료했습니다.",
        data=await user_service.is_duplicate_nickname(data.nickname),
    )

@router.post(
    "/register",
    response_model=ResponseRegister,
)
@inject
async def register(
    nickname: Annotated[str, Form(description="닉네임", example="닉네임")],
    password: Annotated[str, Form(description="비밀번호", example="비밀번호")],
    password1: Annotated[str, Form(description="비밀번호 확인", example="비밀번호 확인")],
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    return ResponseRegister(
        code=status.HTTP_200_OK,
        message="회원가입이 완료되었습니다.",
        data=await user_service.register(
            RequestRegisterDto(
                nickname=nickname,
                password=password,
                password1=password1,
            )
        )
    )

@router.post("/login", response_model=ResponseUser)
@inject
async def login(
nickname: Annotated[str, Form(description="닉네임", example="닉네임")],
    password: Annotated[str, Form(description="비밀번호", example="비밀번호")],
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    # eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMiJ9.-HSiApoYzM87wa8-mRPxZs0vwNjQBCVMLTmROOD5-1A
    return ResponseUser(
        code=status.HTTP_200_OK,
        message="사용자 조회를 완료했습니다.",
        data=await user_service.get_user(current_user),
    )
