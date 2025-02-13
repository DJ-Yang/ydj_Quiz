from typing import Any

from pydantic import BaseModel, Field


class ResponseBaseModel(BaseModel):
    code: int
    message: str


class ResponseBase(ResponseBaseModel):
    data: dict[str, Any] = Field(default={})
