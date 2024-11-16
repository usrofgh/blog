from fastapi import status
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from back.dependencies import get_current_user
from back.exceptions.auth_exceptions import AuthException, IncorrectCredsException
from back.exceptions.user_exceptions import UserForbiddenException
from back.schemas.user_schemas import UserLoginSchema
from back.services.user_service import UserService
from database import SessionLocal


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        async with SessionLocal() as db:
            user_data = UserLoginSchema(username=username, password=password)
            try:
                token = await UserService.login(db=db, user_data=user_data)
            except IncorrectCredsException:
                return False
            request.session.update({"access_token": token.access_token})
        return True

    async def logout(self, request: Request) -> RedirectResponse:
        request.session.clear()
        return RedirectResponse(request.url_for("admin:login"), status_code=status.HTTP_301_MOVED_PERMANENTLY)

    async def authenticate(self, request: Request):
        token = request.session.get("access_token")
        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=status.HTTP_301_MOVED_PERMANENTLY)
        async with SessionLocal() as db:
            try:
                await get_current_user(token, db)
            except (UserForbiddenException, IncorrectCredsException, AuthException):
                return RedirectResponse(request.url_for("admin:login"), status_code=status.HTTP_301_MOVED_PERMANENTLY)
        return True


authentication_backend = AdminAuth(secret_key="...")
