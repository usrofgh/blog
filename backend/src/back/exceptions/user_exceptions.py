from fastapi import status

from back.exceptions.base_exception import BException


class UserEmailExistException(BException):
    STATUS_CODE = status.HTTP_409_CONFLICT
    DETAIL = "User with such email already exists"


class UserNameExistException(BException):
    STATUS_CODE = status.HTTP_409_CONFLICT
    DETAIL = "User with such username already exists"


class UserNotFoundException(BException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "User not found"


class UserForbiddenException(BException):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = "Not enough rules for this action"


class IncorrectActivationLink(BException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Incorrect activation link"


class UnactivatedException(BException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Activate the account"


class PasswordMismatchException(BException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Passwords do not match"

class PasswordNotProperException(BException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Password must contain at least: one uppercase letter, one special character, one digit"


class UsernameSpecialSymbolsException(BException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Username can only contain alphanumeric characters and underscores"

class InvalidEmailException(BException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Invalid Email"


class BlockedAccountException(BException):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = "Account is blocked"


class IncorrectAvatarException(BException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Unsupported file type"


class AvatarDoesNotExist(BException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Avatar does not exist"
