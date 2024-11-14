from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from exceptions.bad_request_exception import BadRequestException
from exceptions.resource_not_found_exception import ResourceNotFoundException
from config.settings import logger


class ExceptionHandler:
    @staticmethod
    def handle_exception(exc: Exception, request: Request = None) -> JSONResponse:

        if isinstance(exc, ResourceNotFoundException):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, content={"message": exc.detail}
            )
        elif isinstance(exc, RequestValidationError):
            logger.debug(f"Validation error : {exc.errors()}")
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"detail": str(exc)},
            )
        elif isinstance(exc, ValidationError):
            logger.debug(f"Validation error: {exc.errors()}")
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"detail": str(exc)},
            )
        elif isinstance(exc, BadRequestException):
            logger.debug(f"Bad request: {exc}")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, content={"message": exc.detail}
            )
        else:
            logger.error(f"Internal server error: {exc}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": "Internal server error"},
            )
