from typing import Annotated
from fastapi import APIRouter, Body, Depends, Form
from dependency_injector.wiring import Provide, inject
from fastapi.security import HTTPBearer
from starlette import status

from app.containers import Container

from app.service.auth import AuthService
from app.service.quiz import QuizService

from app.schemas.quiz import ProblemListResponse, ProblemResponse, RequestProblemDto


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