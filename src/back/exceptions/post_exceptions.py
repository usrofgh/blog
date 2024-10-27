from fastapi import status

from src.back.exceptions.base_exception import BException


class PostNotFoundException(BException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "The post with such id is not found"
