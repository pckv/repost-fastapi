"""API schemas for error responses."""


from pydantic.main import BaseModel


class ErrorResponse(BaseModel):
    """Schema for the common error model"""
    detail: str
