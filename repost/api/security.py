"""Secure utility functions and setup."""

from datetime import timedelta, datetime
from typing import List

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

from repost import config

oauth2_scopes = {'user': 'User access'}

# NOTE: this path is hardcoded and correlates to repost.api.routes.auth.login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/token', scopes=oauth2_scopes)


def create_jwt_token(username: str, expire_delta: timedelta = timedelta(days=7), scopes: List[str] = None) -> str:
    """Create JSON Web Token with a username as the subject"""
    expire = datetime.utcnow() + expire_delta

    data = {'sub': username, 'exp': expire, 'scopes': scopes or []}
    jwt_token = jwt.encode(data, config.jwt_secret, algorithm=config.jwt_algorithm)
    return jwt_token


def decode_jwt_token(jwt_token: str) -> dict:
    """Decode a JSON Web Token"""
    return jwt.decode(jwt_token, key=config.jwt_secret, verify=config.jwt_algorithm)


async def authorize_user(security_scopes: SecurityScopes, jwt_token: str = Depends(oauth2_scheme)) -> str:
    """Validate and return the username in the JSON Web Token."""
    try:
        payload = decode_jwt_token(jwt_token)
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='The JSON Web Token has expired')
    except jwt.exceptions.DecodeError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'Failed to parse JSON Web Token: {str(e)}')

    # Verify that the user has the required scopes for this endpoint
    scopes = payload.get('scopes', [])
    for scope in security_scopes.scopes:
        if scope not in scopes:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Missing scope \'{scope}\'')

    return payload.get('sub')
