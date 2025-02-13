import re
from typing import Awaitable, Callable

from fastapi import Request
from starlette.responses import JSONResponse, StreamingResponse

from app.config import settings
from app.errors import APIException
from starlette import status

import logging

logger = logging.getLogger(__name__)


async def base_http_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[StreamingResponse]]
) -> StreamingResponse | JSONResponse:
    try:
        response = await call_next(request)
        if response.status_code == status.HTTP_403_FORBIDDEN:
            status_code = status.HTTP_403_FORBIDDEN
            error_dict = {
                "status_code": status_code,
                "message": "권한이 없습니다.",
            }
            return JSONResponse(status_code=status_code, content=error_dict)
        return response
    except Exception as e:
        error = await exception_handler(e)
        error_dict = {
            "status_code": error.status_code,
            "message": error.message,
        }
        return JSONResponse(status_code=error.status_code, content=error_dict)


async def url_pattern_check(path: str, pattern: str) -> bool:
    result = re.match(pattern, path)
    if result:
        return True
    return False


async def exception_handler(error: Exception) -> APIException:
    if not isinstance(error, APIException):
        logger.info(error)
        error = APIException()
    return error
