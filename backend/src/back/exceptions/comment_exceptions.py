from fastapi import status

from back.exceptions.base_exception import BException


class CommentNotFoundException(BException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "The comment with such id is not found"


class CommentOlderThanOneDayError(BException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Cannot modify. The comment is older than 1 day"


class ParentCommentDoesNotExistException(BException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Parent comment not found"
