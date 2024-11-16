import pytest
from fastapi import status


class TestPostAPI:
    @pytest.mark.parametrize(
        "post_id, status_code",
        [
            (1, status.HTTP_200_OK),
            (545435, status.HTTP_404_NOT_FOUND)
        ],
        ids=[
            "The post info should be found",
            "The post info should not be found",
        ]
    )
    async def test_read_post(self, post_id: int, status_code: int, auth_admin_ac):
        response = await auth_admin_ac.get(f"/v1/api/posts/{post_id}")
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "status_code",
        [
            status.HTTP_200_OK
        ],
        ids=[
            "The posts info should be displayed",
        ]
    )
    async def test_read_posts(self, status_code: int, auth_admin_ac):
        response = await auth_admin_ac.get("/v1/api/posts/")
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "post_id, status_code",
        [
            (1, status.HTTP_204_NO_CONTENT),
            (54354354, status.HTTP_404_NOT_FOUND)
        ],

        ids=[
            "The post should be deleted",
            "The post should not be deleted",
        ]
    )
    async def test_delete_post(self, post_id: int, status_code: int, auth_admin_ac):
        response = await auth_admin_ac.delete(f"/v1/api/posts/{post_id}")
        assert response.status_code == status_code
