"""Secure utility functions and setup."""

from datetime import timedelta, datetime

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from repost import config

# NOTE: this path is hardcoded and correlates to repost.api.routes.auth.login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/token')


def create_jwt_token(username: str, expire_delta: timedelta = timedelta(days=7)) -> str:
    """Create JSON Web Token with a username as the subject"""
    expire = datetime.utcnow() + expire_delta

    data = {'sub': username, 'exp': expire}
    jwt_token = jwt.encode(data, config.jwt_secret, algorithm=config.jwt_algorithm)
    return jwt_token


def get_jwt_token_username(jwt_token: str) -> str:
    """Get username by decoding JSON Web Token"""
    data = jwt.decode(jwt_token, config.jwt_secret, config.jwt_algorithm)
    username = data.get('sub')
    return username


async def authorize_user(jwt_token: str = Depends(oauth2_scheme)) -> str:
    """Validate and return the username in the JSON Web Token."""
    try:
        return get_jwt_token_username(jwt_token)
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='The JSON Web Token has expired')
    except jwt.exceptions.DecodeError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f'Failed to parse JSON Web Token: {str(e)}')
