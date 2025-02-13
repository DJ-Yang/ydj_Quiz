from app.repository.quiz import QuizRepository

from app.schemas.quiz import (
    SelectionDto,
    ProblemDto,
    RequestProblemDto,
    ProblemUpdateDto,
)


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

        for selection in problem.selections:
            print(selection)

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

    async def create_problem(self, data: RequestProblemDto):
        # TODO: 한개 이상의 데이터가 정답이여야함 / 수정될 때도 마찬가지
        created_problem = await self._repository.create_problem(data)

        return await self.get_problem(created_problem.id)

    async def delete_problem(self, problem_id: int, current_user: int):
        await self._repository.delete_problem(problem_id=problem_id)
        return await self.get_problem_list(current_user)

    async def update_problem(self, problem_id: int, data: ProblemUpdateDto):
        updated_problem = await self._repository.update_problem(problem_id=problem_id, data=data)
        return await self.get_problem(updated_problem.id)
