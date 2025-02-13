from enum import Enum
from typing import Optional
from datetime import datetime

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
    title: Optional[str] = None
    selections: Optional[list[SelectionDto]] = None
