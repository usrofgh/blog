from exceptions.base_exception import BException
from fastapi import status


class ConnectionYourselfException(BException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "You cannot follow/unfollow yourself"


class ConnectionNotExistException(BException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "The connection not found"


class ConnectionStatusException(BException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Must be accepted or rejected"


class ConnectionFailedException(BException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Failed Request"

class IncorrectStatusException(BException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Incorrect status"
