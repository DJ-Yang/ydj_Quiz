from enum import Enum
from typing import Optional
from datetime import datetime

from pydantic import BaseModel

from app.schemas.base import ResponseBaseModel


class ResponseValidateDto(BaseModel):
    is_duplicated: bool


class ResponseValidate(ResponseBaseModel):
    data: ResponseValidateDto


class RequestRegisterDto(BaseModel):
    nickname: str
    password: str
    password1: str


class RequestLoginDto(BaseModel):
    nickname: str
    password: str  


class ResponseUserDto(BaseModel):
    user_id: int
    nickname: str
    token: str
    created_dt: datetime


class ResponseRegister(ResponseBaseModel):
    data: ResponseUserDto


class ResponseUser(ResponseBaseModel):
    data: ResponseUserDto


class ResponseLoginDto(BaseModel):
    user_id: int



class ValidateNickname(BaseModel):
    nickname: str

