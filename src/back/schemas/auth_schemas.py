from pydantic import BaseModel


class JWTLoginResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenCreateSchema(BaseModel):
    user_id: int
    refresh_token: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str
