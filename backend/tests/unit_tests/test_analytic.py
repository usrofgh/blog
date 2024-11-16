import datetime

import pytest

from backend.src.back import CommentFilterSchema
from backend.src.back.services.analytic_service import AnalyticService


class TestAnalytic:
    @pytest.mark.parametrize(
        "date_from, date_to, expected",
        [
            ("2024-10-01", "2024-10-04", [{"created_at": datetime.date(2024, 10, 1), "total_count": 7, "blocked_count": 2, "passed_count": 5}, {"created_at": datetime.date(2024, 10, 3), "total_count": 3, "blocked_count": 0, "passed_count": 3}]),
            ("2024-10-01", "2024-10-01", [{"created_at": datetime.date(2024, 10, 1), "total_count": 7, "blocked_count": 2, "passed_count": 5}]),
            ("2024-10-03", "2024-10-03", [{"created_at": datetime.date(2024, 10, 3), "total_count": 3, "blocked_count": 0, "passed_count": 3}]),
            ("2024-10-02", "2024-10-02", []),
        ],
        ids=[
            "Answer should be with 2 days",
            "Answer should return one value",
            "Answer should return one value",
            "Answer should return empty list"
        ]
    )
    async def test_comment_daily_breakdown_router(self, date_from: str, date_to: str, expected: list[dict], db_session):
        to_format = "%Y-%m-%d"
        date_from = datetime.datetime.strptime(date_from, to_format)
        date_to = datetime.datetime.strptime(date_to, to_format)

        schema = CommentFilterSchema(date_from=date_from, date_to=date_to)
        response = await AnalyticService.analytic_comments(db=db_session, filters=schema)
        if not expected:
            assert response == []
            return

        response = [r.model_dump() for r in response]
        assert response == expected
