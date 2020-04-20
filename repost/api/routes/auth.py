"""Router for authorization."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from repost import crud
from repost.api.resolvers import get_db
from repost.api.schemas import OAuth2Token, ErrorResponse
from repost.api.security import create_jwt_token
from repost.password import verify_password

router = APIRouter()


@router.post('/token', response_model=OAuth2Token,
             responses={status.HTTP_401_UNAUTHORIZED: {'model': ErrorResponse}})
async def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends(),
                authorization: str = Header(None)):
    """Authorize using username and password."""
    client_id = form_data.client_id
    if not client_id and authorization:
        http_basic_auth = b64decode(authorization.replace('Basic ', '')).decode('ascii')
        client_id = http_basic_auth.split(':')[0]

    if not client_id or client_id != config.client_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid client')

    db_user = crud.get_user(db, username=form_data.username)
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid login information')

    return OAuth2Token(access_token=create_jwt_token(username=db_user.username), token_type='bearer')
