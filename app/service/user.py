import logging

from app.repository.user import UserRepository
from app.service.auth import AuthService
from app.schemas.user import ResponseValidateDto, RequestRegisterDto, ResponseUserDto, ResponseLoginDto, RequestLoginDto

from app.errors import UserNotExistError, ValidationError

logger = logging.getLogger(__name__)


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        auth_service: AuthService,
    ) -> None:
        self._repository: UserRepository = user_repository
        self.auth_service: AuthService = auth_service

    async def is_duplicate_nickname(self, nickname) -> ResponseValidateDto:
        logger.info("로깅 테스트")
        duplicate_user = await self._repository.is_duplicate_nickname(nickname)
        return ResponseValidateDto(is_duplicated=duplicate_user is not None)

    async def register(self, register_dto: RequestRegisterDto):
        if register_dto.password != register_dto.password1:
            raise ValidationError("패스워드가 일치하지 않습니다.")

        created_user = await self._repository.create_user(
            nickname=register_dto.nickname,
            password=register_dto.password,
        )
        return ResponseUserDto(
            user_id=created_user.id,
            nickname=created_user.nickname,
            token=self.auth_service.create_access_token(created_user.id),
            created_dt=created_user.created_dt,
        )

    async def login(self, data: RequestLoginDto) -> ResponseUserDto:
        user = await self._repository.get_user_or_none(data)
        if user is None:
            raise UserNotExistError()

        return ResponseUserDto(
            user_id=user.id,
            nickname=user.nickname,
            token=self.auth_service.create_access_token(user.id),
            created_dt=user.created_dt,
        )

    async def get_user_id_from_token(self, token: str) -> ResponseLoginDto:
        return ResponseLoginDto(user_id=self.auth_service.get_user_id_from_token(token))
