from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy import insert, select, update, and_
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.quiz import Problem, UserProblemForm, Selection
from app.schemas.quiz import RequestProblemDto, ProblemUpdateDto
from app.errors import ProblemNotExistError


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
            stmt = select(Problem).where(Problem.id == problem_id).options(selectinload(Problem.selections))
            result = await session.execute(stmt)
            problem = result.scalars().one_or_none()

            if not problem:
                raise ProblemNotExistError()

            problem.title = data.title

            existing_selection_ids = {selection.id for selection in problem.selections}
            new_selection_ids = {selection.id for selection in data.selections if selection.id is not None}

            to_delete = existing_selection_ids - new_selection_ids
            if to_delete:
                await session.execute(
                    Selection.__table__.delete().where(Selection.id.in_(to_delete))
                )

            # TODO: 여기 코드가 너무 비효율적인 것 같은데 좋은 방법이 생각이 안난다.
            for selection_data in data.selections:
                if selection_data.id is not None:
                    for selection in problem.selections:
                        if selection.id == selection_data.id:
                            selection.content = selection_data.content
                            selection.is_correct = selection_data.is_correct
                            break
                else:
                    new_selection = Selection(
                        content=selection_data.content,
                        is_correct=selection_data.is_correct,
                        problem_id=problem.id
                    )
                    session.add(new_selection)

            await session.commit()
            await session.refresh(problem)
            return problem

    async def get_selection_list(self, problem_id: int, id_list: list):
        async with self.session_factory() as session:
            stmt = (
                select(Selection)
                .where(
                    and_(
                        Selection.problem_id == problem_id,
                        Selection.id.in_(id_list)
                    )
                )
            )
            result = await session.execute(stmt)
            return result.scalars().all()

    async def create_user_submit(self, submit_data: dict):
        async with self.session_factory() as session:
            submit_obj = UserProblemForm(**submit_data)
            session.add(submit_obj)
            await session.commit()
            await session.refresh(submit_obj)
            return submit_obj
        
    async def get_user_submit(self, user_id: int):
        async with self.session_factory() as session:
            stmt = (
                select(UserProblemForm)
                .where(UserProblemForm.user_id == user_id)
                .options(
                    joinedload(UserProblemForm.problem)
                )
            )
            result = await session.execute(stmt)
            return result.scalars().all()
