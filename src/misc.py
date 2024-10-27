from httpx import HTTPError
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from src.logger import logger


def retry_on_failure():  # decorator
    return retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        retry=retry_if_exception_type(HTTPError),
        before_sleep=lambda retry_state: logger.error(retry_state.outcome.exception())
    )
