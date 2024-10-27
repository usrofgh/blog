from fastapi import status

from src.back.exceptions.base_exception import BException


class UserExistException(BException):
    STATUS_CODE = status.HTTP_409_CONFLICT
    DETAIL = "User with such email already exists"


class UserNotFoundException(BException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "User not found"


class UserForbiddenException(BException):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = "Not enough rules for this action"


class IncorrectActivationLink(BException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Incorrect activation link"


class UnactivatedException(BException):
    status = status.HTTP_400_BAD_REQUEST
    detail = "Activate the account"
