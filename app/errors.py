from starlette import status


class APIException(Exception):
    status_code: int
    message: str | None

    def __init__(
        self,
        *,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        message: str | None = "오류가 발생했습니다. 시스템 관리자에게 문의해주세요",
    ):
        self.status_code = status_code
        self.message = message


class UserNotExistError(APIException):
    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, message="해당 사용자는 존재하지 않습니다.")


class InvalidTokenError(APIException):
    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, message="토큰이 유효하지 않습니다.")


class ValidationError(APIException):
    def __init__(self, message: str) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, message=message)


class MatchImpossibleError(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="이미 매칭이 진행중입니다."
        )


class NoMatchingUsersError(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="해당 지역에 매칭 가능한 유저가 존재하지 않습니다."
        )


class NoLocationError(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="매칭을 위해서는 위치 정보를 먼저 등록해주세요."
        )
