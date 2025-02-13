from datetime import date, datetime
from typing import Optional

from sqlalchemy import Enum, String, Integer, DateTime, Boolean, Double, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "user"
    nickname: Mapped[str] = mapped_column(String(20), unique=True, comment="별명")
    password: Mapped[str] = mapped_column(String(100), comment="비밀번호")