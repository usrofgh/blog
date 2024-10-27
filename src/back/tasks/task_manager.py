import smtplib
from email.message import EmailMessage

from arq.connections import RedisSettings
from tenacity import RetryError

from src.back.dao.comment_dao import CommentDAO
from src.back.exceptions.base_exception import NetworkErrorException, SwearWordException
from src.back.models.comments import CommentModel
from src.back.schemas.comment_schemas import CommentCreateDBSchema
from src.config import config
from src.database import SessionLocal
from src.managers.openai_manager import openai_manager
from src.misc import retry_on_failure

REDIS_SETTINGS = RedisSettings(config.REDIS_HOST, config.REDIS_PORT)


@retry_on_failure()
async def auto_reply(
    ctx: dict,
    post_text: str,
    comment_text: str,
    author_id: int, post_id: int,
    parent_comment_id: int = None
) -> CommentModel:
    db = ctx["session"]
    try:
        reply = openai_manager.generate_auto_reply(post_text, comment_text)
    except RetryError:
        raise NetworkErrorException

    swear_words = openai_manager.detect_swear_words(reply)
    comment_data = CommentCreateDBSchema(
        content=reply, post_id=post_id, author_id=author_id,
        is_blocked=bool(swear_words), parent_comment_id=parent_comment_id
    )

    db_comment = await CommentDAO.create_comment(db=db, comment_data=comment_data)
    if swear_words:
        raise SwearWordException

    return db_comment


async def startup(ctx):
    ctx["session"] = SessionLocal()


async def shutdown(ctx):
    await ctx["session"].close()


async def send_activation_email(ctx: dict, to: str, activation_code: str) -> None:
    with smtplib.SMTP_SSL(config.SMTP_HOST, config.SMTP_PORT) as server:
        server.login(
            user=config.SMTP_USER,
            password=config.SMTP_PASSWORD,
        )

        email = EmailMessage()
        email["Subject"] = "Activation link"
        email["From"] = config.SMTP_USER
        email["To"] = to
        link = f"http://127.0.0.1:8000/v1/api/auth/activate-account/?activation_code={activation_code}"
        email.set_content(
            f"""
                <div>
                    <a href='{link}'>Activation link</a>
                </div>
                """,
            subtype="html"
        )
        server.send_message(email)


class WorkerSettings:
    functions = [auto_reply, send_activation_email]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = REDIS_SETTINGS
    max_jobs = 10
    keep_result = False  # Don't save result to redis. It'll be saved to psql db
