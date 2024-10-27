import sentry_sdk
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from redis import asyncio as aioredis
from sqladmin import Admin

from src.back.admin_panel.auth import authentication_backend
from src.back.admin_panel.views import CommentAdmin, PostAdmin, UserAdmin
from src.back.routers.analytic_router import analytic_router
from src.back.routers.auth_router import auth_router
from src.back.routers.comment_router import comment_router
from src.back.routers.post_router import post_router
from src.back.routers.user_router import user_router
from src.config import Envs, config
from src.database import engine

if config.MODE is not Envs.TEST:  # During testing process we don't need to log errors
    # Example of the error description - https://prnt.sc/Iso5oQqEkMOO
    sentry_sdk.init(
        dsn=config.SENTRY_DSN,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        traces_sample_rate=config.SENTRY_RATE,
        _experiments={
            # Set continuous_profiling_auto_start to True
            # to automatically start the profiler on when
            # possible.
            "continuous_profiling_auto_start": True,
        },
    )

app = FastAPI(
    title="Blog",
    summary="The blog allows creating posts and comment them"
)

app.include_router(auth_router)
app.include_router(analytic_router)
app.include_router(user_router)
app.include_router(post_router)
app.include_router(comment_router)

app = VersionedFastAPI(
    app=app,
    version_format="{major}",
    prefix_format="/v{major}",
)

admin_panel = Admin(
    app=app,
    engine=engine,
    authentication_backend=authentication_backend
)
admin_panel.add_view(UserAdmin)
admin_panel.add_view(PostAdmin)
admin_panel.add_view(CommentAdmin)


@app.on_event("startup")
def startup():
    redis = aioredis.from_url(config.REDIS_URI)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
