from datetime import date

from pydantic import BaseModel, Field


class AnalyticCommentSchema(BaseModel):
    created_at: date
    total_count: int
    blocked_count: int
    passed_count: int


class AnalyticCommentFilterSchema(BaseModel):
    date_from: date = Field(default=date(2024, 1, 24))
    date_to: date = Field(default=date(2024, 10, 25))
