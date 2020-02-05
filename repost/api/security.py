"""Secure utility functions and setup."""
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer


# NOTE: this path is hardcoded and correlates to repost.api.routes.auth.login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/token')


async def authorize_user(token: str = Depends(oauth2_scheme)):
    """Validate and return the username in the JSON Web Token."""
    pass


async def get_current_user(username: str = Depends(authorize_user)):
    """Resolve the user with the given username."""
    pass
