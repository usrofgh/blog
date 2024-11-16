from fastapi import HTTPException, status


class BException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = None

    def __init__(self) -> None:
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL)


class SwearWordException(BException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Swear word detected"


class NetworkErrorException(BException):
    STATUS_CODE = status.HTTP_408_REQUEST_TIMEOUT
    DETAIL = "Error. Try again"
