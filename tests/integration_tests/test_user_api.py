import pytest
from fastapi import status


class TestUserAPI:
    @pytest.mark.parametrize(
        "email, password, status_code",
        [
            ("admin@blog.com", "string", status.HTTP_200_OK),
            ("not_activated_user@blog.com", "string", status.HTTP_400_BAD_REQUEST),
            ("absent_email@blog.com", "string", status.HTTP_401_UNAUTHORIZED),
        ],
        ids=[
            "The user should login",
            "The user should not login without activation by email",
            "The absent user should not login"
        ]
    )
    async def test_login_user(self, email: str, password: str, status_code: int, ac):
        data = {
            "email": email,
            "password": password,
        }
        response = await ac.post("/v1/api/auth/login", json=data)
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "user_id, response_code",
        [
            (1, status.HTTP_204_NO_CONTENT),
        ],
        ids=[
            "The user should be deleted",
        ]
    )
    async def test_delete_user(self, user_id: int, response_code: int, auth_admin_ac):
        response = await auth_admin_ac.delete(f"/v1/api/users/{user_id}")
        assert response.status_code == response_code
