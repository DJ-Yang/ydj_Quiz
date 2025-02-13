from app.repository.user import UserRepository
from app.service.auth import AuthService
from app.schemas.user import ResponseValidateDto, RequestRegisterDto, ResponseRegisterDto, ResponseUserDto, ResponseLoginDto

from app.errors import UserNotExistError, ValidationError


FIVE_MEGA = 1024 * 1024 * 5

class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        auth_service: AuthService,
    ) -> None:
        self._repository: UserRepository = user_repository
        self.auth_service: AuthService = auth_service

    async def is_duplicate_nickname(self, nickname) -> ResponseValidateDto:
        duplicate_user = await self._repository.is_duplicate_nickname(nickname)
        return ResponseValidateDto(is_duplicated=duplicate_user is not None)

    async def register(self, register_dto: RequestRegisterDto) -> None:
        if register_dto.password != register_dto.password1:
            raise

        created_user = await self._repository.create_user(
            register_dto.nickname,
        )
        return ResponseRegisterDto(
            user_id=created_user.id,
            nickname=created_user.nickname,
            token=self.auth_service.create_access_token(created_user.id),
        )

    async def get_user(self, user_id: int) -> ResponseUserDto:
        user = await self._repository.get_user_or_none(user_id)
        if user is None:
            raise UserNotExistError()

        return ResponseUserDto(
            nickname=user.nickname,
            token=self.auth_service.create_access_token(user.id),
            created_dt=user.created_dt,
        )

    async def get_user_id_from_token(self, token: str) -> ResponseLoginDto:
        return ResponseLoginDto(user_id=self.auth_service.get_user_id_from_token(token))
