"""Router for authorization."""
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from repost.api.schemas import OAuth2Token

router = APIRouter()


@router.post('/token', response_model=OAuth2Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authorize using username and password."""
    pass
