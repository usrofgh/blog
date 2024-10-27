from fastapi import status
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.back.dependencies import get_current_user
from src.back.exceptions.auth_exceptions import AuthException, IncorrectCredsException
from src.back.exceptions.user_exceptions import UserForbiddenException
from src.back.schemas.user_schemas import UserLoginSchema
from src.back.services.user_service import UserService
from src.database import SessionLocal


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        async with SessionLocal() as db:
            user_data = UserLoginSchema(email=email, password=password)
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
