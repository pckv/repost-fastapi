"""Secure utility functions and setup."""

import os
from datetime import timedelta, datetime

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

JWT_SECRET = os.getenv('JWT_SECRET')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')

# NOTE: this path is hardcoded and correlates to repost.api.routes.auth.login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/token')


async def authorize_user(token: str = Depends(oauth2_scheme)):
    """Validate and return the username in the JSON Web Token."""
    pass


async def get_current_user(username: str = Depends(authorize_user)):
    """Resolve the user with the given username."""
    pass


def create_jwt_token(username: str, expire_delta: timedelta = timedelta(days=7)) -> str:
    """Create JSON Web Token with a username as the subject"""
    expire = datetime.utcnow() + expire_delta

    data = {'sub': username, 'exp': expire}
    jwt_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return jwt_token


def get_jwt_token_username(jwt_token: str) -> str:
    data = jwt.decode(jwt_token, JWT_SECRET, JWT_ALGORITHM)
    username = data.get('sub')
    return username
