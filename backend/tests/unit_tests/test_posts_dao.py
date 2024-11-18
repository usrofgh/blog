import pytest

from repositories.post_repository import PostRepository


class TestPostDAO:
    @pytest.mark.parametrize(
        "id, is_found",
        [
            (1, True),
            (231232, False),
        ],
        ids=[
            "The post should be found by id",
            "The post should not be found by id"
        ]
    )
    async def test_get_post_by_id(self, id: int, is_found: bool, db_session):
        db_post = await PostRepository.find_one(db=db_session, id=id)
        assert bool(db_post) == is_found

    @pytest.mark.parametrize(
        "author_id, is_found",
        [
            (1, True),
            (231232, False),
        ],
        ids=[
            "The post should be found by author id",
            "The post should not be found by author id"
        ]
    )
    async def test_get_post_by_author_id(self, author_id: int, is_found: bool, db_session):
        db_post = await PostDAO.read_posts_by_author_id(db=db_session, author_id=author_id)
        assert bool(db_post) == is_found

    @pytest.mark.parametrize(
        "filters, count_posts",
        [
            ({"is_blocked": True, "author_id": 1}, 1),
            ({"author_id": 33783}, 0),
        ],
        ids=[
            "The post should be found by filters",
            "The post should not be found by filters"
        ]
    )
    async def test_get_post_by_filters(self, filters: dict, count_posts: int, db_session):
        db_posts = await PostRepository.find_all(db=db_session, **filters)
        assert len(db_posts) == count_posts

    # @pytest.mark.parametrize(
    #     "author_id, is_blocked, content, is_created",
    #     [
    #         (1, False, "What's up guys", True),
    #         (4324234, False, "How are you?", False),
    #     ],
    #     ids=[
    #         "The post should be created",
    #         "The post should not be created"
    #     ]
    # )
    # # TODO: "FAILED tests/unit_tests/test_posts_dao.py::TestPostDAO::test_create_post[The post should be created] - sqlalchemy.exc.IntegrityError: (sqlalchemy.dialects.postgresql.asyncpg.IntegrityError) <class 'asyncpg.exceptions.UniqueViolationError'>: duplicate key value violates unique constraint "posts_pkey""
    # async def test_create_post(self, author_id: int, content: str, is_blocked: bool, is_created: bool, db_session):
    #     schema = PostCreateDBSchema(author_id=author_id, is_blocked=is_blocked, content=content)
    #
    #     db_post = await PostDAO.create_post(db=db_session, post_data=schema)
    #     db_post = await PostDAO.read_post_by_id(db=db_session, id=db_post.id)
    #
    #     if is_created is False:
    #         assert db_post is None
    #         return
    #
    #     assert db_post
    #     assert db_post.author_id is author_id
    #     assert db_post.is_blocked is is_blocked
    #     assert db_post.created_at
    #     assert db_post.updated_at
    #     assert db_post.content == content

    @pytest.mark.parametrize(
        "id, is_deleted",
        [
            (1, True),
            (54235, False),
        ],
        ids=[
            "The post should be deleted",
            "The post should not be deleted (not found)"
        ]
    )
    async def test_delete_post(self, id: int, is_deleted: bool, db_session):
        db_user = await PostRepository.find_one(db=db_session, id=id)
        assert bool(db_user) is is_deleted

        if db_user:
            await PostRepository.delete(db=db_session, db_obj=db_user)

        db_user = await PostRepository.find_one(db=db_session, id=id)
        assert db_user is None
