from pydantic.main import BaseModel


class ErrorResponse(BaseModel):
    detail: str
