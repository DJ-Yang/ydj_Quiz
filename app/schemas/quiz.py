from typing import Optional

from pydantic import BaseModel

from app.schemas.base import ResponseBaseModel


class SelectionDto(BaseModel):
    id: int
    content: str
    is_correct: Optional[bool] = None


class ProblemDto(BaseModel):
    id: int
    title: str
    selections: Optional[list[SelectionDto]]


class ProblemListResponse(ResponseBaseModel):
    data: list[ProblemDto]


class ProblemResponse(ResponseBaseModel):
    data: ProblemDto


class RequestSelectionDto(BaseModel):
    content: str
    is_correct: bool


class RequestProblemDto(BaseModel):
    title: str
    selections: list[RequestSelectionDto]


class ProblemUpdateDto(BaseModel):
    title: str
    selections: list[SelectionDto]


# TODO: 나중에 한 퀴즈에 하나의 문제가 아니라 두개 이상일 수도 있겠다.
class ProblemSubmitDto(BaseModel):
    answer_list: list[int]


class UserSubmitDto(BaseModel):
    problem_id: int
    title: str
    selections: list[SelectionDto]


class SumbitResponse(ResponseBaseModel):
    data: UserSubmitDto


class SubmitListResponse(ResponseBaseModel):
    data: dict