from contextlib import AbstractAsyncContextManager
from typing import Callable, Optional

from sqlalchemy import insert, select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.quiz import Problem, UserProblemForm, Selection
from app.schemas.quiz import RequestProblemDto, ProblemUpdateDto


class QuizRepository:
    def __init__(
        self, 
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]
    ) -> None:
        self.session_factory = session_factory

    async def create_problem(self, data: RequestProblemDto):
        async with self.session_factory() as session:
            problem = Problem(
                title=data.title
            )
            session.add(problem)
            await session.flush()
            await session.refresh(problem)

            await session.execute(insert(Selection).values([
                {
                    "problem_id": problem.id,
                    "content": selection.content,
                    "is_correct": selection.is_correct,
                }
                for selection in data.selections
            ]))
            await session.commit()
            return problem

    async def get_problem_list(self, current_user: int):
        async with self.session_factory() as session:
            stmt = (
                select(Problem)
            )
            result = await session.execute(stmt)
            return result.scalars().all()

    async def delete_problem(self, problem_id: int):
        async with self.session_factory() as session:
            stmt = select(Problem).where(Problem.id == problem_id)
            result = await session.execute(stmt)
            problem = result.scalars().one_or_none()

            if not problem:
                raise ValueError("Problem not found")

            await session.delete(problem)
            await session.commit()

    async def get_problem_detail(self, problem_id: int):
        async with self.session_factory() as session:
            stmt = (
                select(Problem)
                .where(Problem.id == problem_id)
                .options(
                    selectinload(Problem.selections)
                )
            )
            result = await session.execute(stmt)
            return result.scalars().one_or_none()

    async def update_problem(self, problem_id: int, data: ProblemUpdateDto):
        async with self.session_factory() as session:
            stmt = select(Problem).where(Problem.id == problem_id)
            result = await session.execute(stmt)
            problem = result.scalars().one_or_none()

            if not problem:
                raise HTTPException(status_code=404, detail="Problem not found")

            if data.title is not None:
                problem.title = data.title

            if data.selections:
                for selection_data in data.selections:
                    stmt = select(Selection).where(
                        Selection.id == selection_data.id,  # ID 기준으로 찾음
                        Selection.problem_id == problem_id  # 문제와 연결된 선택지인지 확인
                    )
                    result = await session.execute(stmt)
                    selection = result.scalars().one_or_none()

                    if not selection:
                        raise HTTPException(status_code=404, detail=f"Selection {selection_data.id} not found")

                    if selection_data.content is not None:
                        selection.content = selection_data.content
                    if selection_data.is_correct is not None:
                        selection.is_correct = selection_data.is_correct

            await session.commit()
            await session.refresh(problem)
            return problem