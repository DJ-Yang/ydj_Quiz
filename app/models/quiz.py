from datetime import date, datetime
from typing import Optional

from sqlalchemy import Enum, String, Integer, DateTime, Boolean, Double, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Problem(BaseModel):
    __tablename__ = "problem"
    title: Mapped[str] = mapped_column(String(256), nullable=False, comment="문제 제목")

    selections: Mapped[list["Selection"]] = relationship(back_populates="problem", cascade="all, delete")
    users: Mapped[list["UserProblemForm"]] = relationship(back_populates="problem", cascade="all, delete")


class UserProblemForm(BaseModel):
    __tablename__ = "user_problem_form"
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), comment="작성자 ID")
    problem_id: Mapped[int] = mapped_column(ForeignKey("problem.id", ondelete="CASCADE"), comment="문제 ID")
    choices: Mapped[str] = mapped_column(Text, comment="제출지")
    score: Mapped[str] = mapped_column(String(8), nullable=True, comment="점수")

    problem: Mapped["Problem"] = relationship(back_populates="users")
    user: Mapped["User"] = relationship(back_populates="problems")


# TODO: 퀴즈가 수정될 경우 어떻게 헤야하지..? 정답지 번호가 바꾸면 점수 전부 다시 책정..?
# 정답이 여러 개일 경우도 고려해서 정답 필드를 선택지에 포함.
class Selection(BaseModel):
    __tablename__ = "selection"
    problem_id: Mapped[int] = mapped_column(ForeignKey("problem.id", ondelete="CASCADE"), comment="문제 ID")
    content: Mapped[str] = mapped_column(String(256), nullable=False, comment="문제 보기")
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False, comment="정답 여부")

    problem: Mapped["Problem"] = relationship(back_populates="selections")
