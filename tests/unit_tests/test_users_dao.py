import pytest

from src.back.dao.user_dao import UserDAO


class TestUserDAO:
    @pytest.mark.parametrize(
        "user_id, is_found",
        [
            (1, True),
            (3434, False),
        ],
        ids=[
            "The user should be found by id",
            "The user should not be found by id"
        ]
    )
    async def test_get_user_by_id(self, user_id: int, is_found: bool, db_session):
        db_user = await UserDAO.read_user_by_id(db=db_session, id=user_id)
        assert bool(db_user) == is_found

    @pytest.mark.parametrize(
        "email, is_found",
        [
            ("admin@blog.com", True),
            ("not_found@blog.com", False),
        ],
        ids=[
            "The user should be found by email",
            "The user should not be found by email"
        ]
    )
    async def test_get_user_by_email(self, email: str, is_found: bool, db_session):
        db_user = await UserDAO.read_user_by_email(db=db_session, email=email)
        assert bool(db_user) == is_found

    @pytest.mark.parametrize(
        "act_code, is_found",
        [
            ("1", True),
            ("100", False),
        ],
        ids=[
            "The user should be found by activation code",
            "The user should not be found by activation code"
        ]
    )
    async def test_get_user_by_act_code(self, act_code: str, is_found: bool, db_session):
        db_user = await UserDAO.read_user_by_act_code(db=db_session, activation_code=act_code)
        assert bool(db_user) == is_found

    @pytest.mark.parametrize(
        "filters, count_records",
        [
            ({"auto_reply": False}, 2),
            ({"is_activated": False}, 1),
            ({"auto_reply_sec_delay": 111111}, 0),
        ],
        ids=[
            "The users should be found by auto_reply column",
            "The users should not be found by 'is_activated' column",
            "The users should not be found by 'auto_reply_sec_delay' column",
        ]
    )
    async def test_get_users_by_filters(self, filters: dict, count_records: int, db_session):
        db_users = await UserDAO.read_users(db=db_session, **filters)
        assert len(db_users) == count_records

    # @pytest.mark.parametrize(
    #     "email, password, activation_code, expect_error",
    #     [
    #         ("new_user@blog.com", "string", "act_test", False),
    #         # ("admin@blog.com", "string", "act_test1", True),
    #     ],
    #     ids=[
    #         "The user should be created",
    #         # "The user should not be created",
    #     ]
    # )
    # # TODO "FAILED tests/unit_tests/test_users_dao.py::TestUserDAO::test_create_user[The user should be created] - sqlalchemy.exc.IntegrityError: (sqlalchemy.dialects.postgresql.asyncpg.IntegrityError) <class 'asyncpg.exceptions.UniqueViolationError'>: duplicate key value violates unique constraint "users_pkey""
    # async def test_create_user(self, email: str, password: str, activation_code: str, expect_error: bool, db_session):
    #     schema = UserCreateDBSchema(email=email, password=password, activation_code=activation_code)
    #     if expect_error:
    #         with pytest.raises(IntegrityError):
    #             await UserDAO.create_user(db=db_session, user_data=schema)
    #             return
    #
    #     db_user: UserModel = await UserDAO.create_user(db=db_session, user_data=schema)
    #     assert db_user
    #     assert db_user.email == email
    #     assert AuthService.verify_password(db_user.password, password)
    #     assert db_user.activation_code == activation_code
    #     assert db_user.is_activated is False
    #     assert db_user.is_admin is False
    #     assert db_user.auto_reply is False
    #     assert db_user.auto_reply_sec_delay == 30
    #
    #     found_user = await UserDAO.read_user_by_id(db=db_session, id=db_user.id)
    #     assert bool(found_user)

    @pytest.mark.parametrize(
        "id, is_deleted",
        [
            (1, True),
            (54235, False),
        ],
        ids=[
            "The user should be deleted",
            "The user should not be deleted (not found)"
        ]
    )
    async def test_delete_user(self, id: int, is_deleted: bool, db_session):
        db_user = await UserDAO.read_user_by_id(db=db_session, id=id)
        assert bool(db_user) is is_deleted

        if db_user:
            await UserDAO.delete_user(db=db_session, db_obj=db_user)

        db_user = await UserDAO.read_user_by_id(db=db_session, id=id)
        assert db_user is None
