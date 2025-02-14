from typing import Annotated
from fastapi import APIRouter, Body, Depends, Form
from dependency_injector.wiring import Provide, inject
from fastapi.security import HTTPBearer
from starlette import status

from app.containers import Container

from app.service.auth import AuthService
from app.service.quiz import QuizService

from app.schemas.quiz import (
    ProblemListResponse,
    ProblemResponse,
    RequestProblemDto,
    ProblemUpdateDto,
    ProblemSubmitDto,
    SumbitResponse,
    SubmitListResponse,
)


oauth2_scheme = HTTPBearer()
router = APIRouter(tags=["quiz"])
currentUser = Annotated[str, Depends(AuthService.get_current_user)]


@router.get("/", response_model=ProblemListResponse)
@inject
async def get_problem_list(
    current_user: currentUser,
    quiz_service: QuizService = Depends(Provide[Container.quiz_service]),
):  
    return ProblemListResponse(
        code=status.HTTP_200_OK,
        message="퀴즈 목록을 성공적으로 불러왔습니다.",
        data=await quiz_service.get_problem_list(current_user),
    )

@router.post("/", response_model=ProblemResponse)
@inject
async def create_problem(
    data: RequestProblemDto,
    quiz_service: QuizService = Depends(Provide[Container.quiz_service]),
):
    return ProblemResponse(
        code=status.HTTP_200_OK,
        message="퀴즈를 성공적으로 생성했습니다.",
        data=await quiz_service.create_problem(data)
    )

@router.get("/<id>", response_model=ProblemResponse)
@inject
async def get_problem(
    id: int,
    quiz_service: QuizService = Depends(Provide[Container.quiz_service]),
):
    return ProblemResponse(
        code=status.HTTP_200_OK,
        message="퀴즈를 성공적으로 불러왔습니다.",
        data=await quiz_service.get_problem(id)
    )

@router.delete("/<id>", response_model=ProblemListResponse)
@inject
async def delete_problem(
    id: int,
    current_user: currentUser,
    quiz_service: QuizService = Depends(Provide[Container.quiz_service]),
):
    return ProblemListResponse(
        code=status.HTTP_200_OK,
        message="퀴즈를 성공적으로 삭제했습니다.",
        data=await quiz_service.delete_problem(id, current_user)
    )

@router.put("/<id>", response_model=ProblemResponse)
@inject
async def update_problem(
    id: int,
    data: ProblemUpdateDto,
    quiz_service: QuizService = Depends(Provide[Container.quiz_service]),
):
    return ProblemResponse(
        code=status.HTTP_200_OK,
        message="퀴즈를 성공적으로 삭제했습니다.",
        data=await quiz_service.update_problem(id, data)
    )

@router.post("/<id>/submit", response_model=SumbitResponse)
@inject
async def submit_problem_answer(
    id: int,
    current_user: currentUser,
    data: ProblemSubmitDto,
    quiz_service: QuizService = Depends(Provide[Container.quiz_service]),

):
    return SumbitResponse(
        code=status.HTTP_200_OK,
        message="정답을 성공적으로 제출했습니다.",
        data=await quiz_service.submit_problem_answer(id, current_user, data)
    )

@router.get("/mypage", response_model=SubmitListResponse)
@inject
async def my_submit_list(
    current_user: currentUser,
    quiz_service: QuizService = Depends(Provide[Container.quiz_service]),
):
    return SubmitListResponse(
        code=status.HTTP_200_OK,
        message="제출한 문제 목록을 불러왔습니다.",
        data=await quiz_service.get_user_submit_list(current_user)
    )