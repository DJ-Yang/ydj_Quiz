from app.repository.quiz import QuizRepository

from app.schemas.quiz import (
    SelectionDto,
    ProblemDto,
    RequestProblemDto,
    ProblemUpdateDto,
    ProblemSubmitDto,
    UserSubmitDto,
)
from app.utils import convert_list_to_str, convert_str_to_list
from app.errors import ProblemNotExistError, ValidationError


class QuizService:
    def __init__(
        self,
        quiz_repository: QuizRepository,
    ) -> None:
        self._repository: QuizRepository = quiz_repository

    async def get_problem_list(self, current_user: int):
        problem_list = await self._repository.get_problem_list(current_user)
        return [
            ProblemDto(
                id=problem.id,
                title=problem.title,
                selections=None
            )
            for problem in problem_list
        ]

    async def get_problem(self, problem_id: int):
        problem = await self._repository.get_problem_detail(problem_id=problem_id)

        if not problem:
            raise ProblemNotExistError()

        return ProblemDto(
            id=problem.id,
            title=problem.title,
            selections=[
                SelectionDto(
                    id=selection.id,
                    content=selection.content,
                    is_correct=selection.is_correct,
                )
                for selection in problem.selections
            ]
        )

    def _check_is_correct_true(self, selection_list: list) -> bool:
        for selection in selection_list:
            if selection.is_correct is True:
                return True
        return False

    async def create_problem(self, data: RequestProblemDto):
        if not self._check_is_correct_true(data.selections):
            raise ValidationError("최소한 1개 이상의 정답이 존재해야 합니다.")

        created_problem = await self._repository.create_problem(data)

        return await self.get_problem(created_problem.id)

    async def delete_problem(self, problem_id: int, current_user: int):
        await self._repository.delete_problem(problem_id=problem_id)
        return await self.get_problem_list(current_user)

    async def update_problem(self, problem_id: int, data: ProblemUpdateDto):
        if not self._check_is_correct_true(data.selections):
            raise ValidationError("최소한 1개 이상의 정답이 존재해야 합니다.")

        updated_problem = await self._repository.update_problem(problem_id=problem_id, data=data)
        return await self.get_problem(updated_problem.id)

    async def submit_problem_answer(self, problem_id: int, user_id: int, data: ProblemSubmitDto):
        problem = await self._repository.get_problem_detail(problem_id=problem_id)
        if not problem:
            raise ProblemNotExistError()

        selections = await self._repository.get_selection_list(problem_id=problem_id, id_list=data.answer_list)
        if not selections:
            raise ValidationError("문제에 없는 보기를 고르셨습니다.")

        count = 0
        selection_dto_list = []
        for selection in selections:
            if selection.is_correct is True:
                count += 1

            selection_dto_list.append(
                SelectionDto(
                    id=selection.id,
                    content=selection.content,
                    is_correct=selection.is_correct,
                )
            )

        submit_data = {
            "user_id": user_id,
            "problem_id": problem_id,
            "choices": convert_list_to_str(data.answer_list),
            "score": 1 if len(data.answer_list) == count else 0
        }

        user_submit_data = await self._repository.create_user_submit(submit_data)

        return UserSubmitDto(
            problem_id=problem_id,
            title=problem.title,
            selections=selection_dto_list,
        )

    async def get_user_submit_list(self, user_id: int):
        user_submit_list = await self._repository.get_user_submit(user_id)

        result = []
        total_score = 0
        for sumit_data in user_submit_list:
            problem = sumit_data.problem

            selections = await self._repository.get_selection_list(
                problem_id=problem.id,
                id_list=convert_str_to_list(sumit_data.choices),
            )

            result.append(
                UserSubmitDto(
                    problem_id=problem.id,
                    title=problem.title,
                    selections=[
                        SelectionDto(
                            id=selection.id,
                            content=selection.content,
                            is_correct=selection.is_correct,
                        ) for selection in selections
                    ]
                )
            )

            total_score += sumit_data.score

        return {
            "uesr_submit_data": result,
            "total_score": total_score
        }
