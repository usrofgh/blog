from fastapi import status

from src.back.exceptions.base_exception import BException


class AuthException(BException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Could not validate credentials"


class IncorrectCredsException(BException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "Incorrect credentials"


class JWTIncorrectFormatException(BException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect JWT token format"


class JWTokenExpiredException(BException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "JWT token expired"
