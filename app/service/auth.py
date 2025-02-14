from jose import jwt
from typing import Annotated

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security

from app.config import settings
from app.errors import InvalidTokenError

oauth2_scheme = HTTPBearer()


class AuthService:
    def __init__(
        self,
        secret_key: str,
    ) -> None:
        self.secret_key = secret_key
        self.algorithms = "HS256"

    def create_access_token(self, user_id: int) -> str:
        return jwt.encode({"user_id": str(user_id)}, self.secret_key)

    def get_user_id_from_token(self, token: str) -> int:
        try:
            payload = jwt.decode(
                token=token,
                key=settings.SECRET_KEY,
                algorithms=self.algorithms,
            )
            user_id: int = int(payload.get("user_id", -1))
            if user_id == -1:
                raise InvalidTokenError()
        except jwt.JWTError as JWTError:
            raise InvalidTokenError() from JWTError
        return user_id

    @staticmethod
    def get_current_user(credentials: Annotated[HTTPAuthorizationCredentials | str, Security(oauth2_scheme)]) -> int:
        try:
            if isinstance(credentials, str):
                payload = jwt.decode(
                    token=credentials,
                    key=settings.SECRET_KEY,
                    algorithms="HS256",
                )
            else:
                payload = jwt.decode(
                    token=credentials.credentials,
                    key=settings.SECRET_KEY,
                    algorithms="HS256",
                )
            user_id: int = int(payload.get("user_id", -1))
            if user_id == -1:
                raise InvalidTokenError()
        except jwt.JWTError as JWTError:
            raise InvalidTokenError() from JWTError
        return user_id
