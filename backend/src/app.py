import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

import sentry_sdk
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from redis import asyncio as aioredis
from sqladmin import Admin

from admin_panel.auth import authentication_backend
from admin_panel.views import CommentAdmin, PostAdmin, UserAdmin
from pages.auth_router import web_router
from routers.analytic_router import analytic_router
from routers.auth_router import auth_router
from routers.comment_router import comment_router
from routers.connection_router import connection_router
from routers.post_router import post_router
from routers.like_router import like_router
from routers.user_router import user_router

from config import config
from database import engine

if config.MODE != "TEST":  # During testing process we don't need to log errors
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
app.include_router(connection_router)
app.include_router(post_router)
app.include_router(comment_router)
app.include_router(like_router)

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
