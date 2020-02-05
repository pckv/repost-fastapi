"""API schemas for authorization."""

from pydantic.main import BaseModel


class OAuth2Token(BaseModel):
    """Schema for an OAuth2 token"""
    access_token: str
    token_type: str
