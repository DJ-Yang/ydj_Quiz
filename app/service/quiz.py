from app.repository.quiz import QuizRepository

from app.schemas.quiz import SelectionDto, ProblemDto, RequestProblemDto


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
                )
                for selection in problem.selections
            ]
        )

    async def create_problem(self, data: RequestProblemDto):
        created_problem = await self._repository.create_problem(data)

        try:
            return await self.get_problem(created_problem.id)
        except Exception as e:
            print("error", e)
