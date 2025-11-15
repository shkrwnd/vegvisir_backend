from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError


class AppException(Exception):
    """Base exception for application-specific errors."""
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(AppException):
    """Exception for resource not found errors."""
    def __init__(self, resource: str, identifier: str = None):
        message = f"{resource} not found"
        if identifier:
            message += f" with id: {identifier}"
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)


class UnauthorizedError(AppException):
    """Exception for unauthorized access errors."""
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)


class ForbiddenError(AppException):
    """Exception for forbidden access errors."""
    def __init__(self, message: str = "Forbidden access"):
        super().__init__(message, status_code=status.HTTP_403_FORBIDDEN)


class ValidationError(AppException):
    """Exception for validation errors."""
    def __init__(self, message: str = "Validation error"):
        super().__init__(message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


async def app_exception_handler(request: Request, exc: AppException):
    """Handler for application-specific exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler for request validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handler for SQLAlchemy database errors."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Database error occurred"}
    )

