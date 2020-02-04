from fastapi import APIRouter

from repost.api.routes import users, auth

api_router = APIRouter()
api_router.include_router(users.router, prefix='/users', tags=['users'])
api_router.include_router(auth.router, prefix='/auth', tags=['auth'])
