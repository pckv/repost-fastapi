"""Routes for all endpoints in the API."""

from fastapi import APIRouter

from repost.api.routes import users, auth, resubs, posts, comments

api_router = APIRouter()
api_router.include_router(auth.router, prefix='/auth', tags=['auth'])
api_router.include_router(users.router, prefix='/users', tags=['users'])
api_router.include_router(resubs.router, prefix='/resubs', tags=['resubs'])
api_router.include_router(posts.router, prefix='/posts', tags=['posts'])
api_router.include_router(comments.router, prefix='/comments', tags=['comments'])
