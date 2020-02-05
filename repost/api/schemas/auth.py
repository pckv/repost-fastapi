"""API schemas for authorization."""

from pydantic.main import BaseModel


class OAuth2Token(BaseModel):
    access_token: str
    token_type: str
