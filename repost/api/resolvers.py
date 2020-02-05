""" Dependencies for resolving and verifying paths and ownership. """

from fastapi import Path, Depends

from repost.api.schemas import Resub, User, Post
from repost.api.security import get_current_user


async def resolve_resub(resub: str = Path(...)) -> Resub:
    """ Verify the resub from path parameter. 404 if not found. """
    pass


async def resolve_user_owned_resub(resub: Resub = Depends(resolve_resub),
                                   current_user: User = Depends(get_current_user)) -> Resub:
    """ Verify that the authorized user owns the resub before returning. """
    pass


async def resolve_post(resub: Resub = Depends(resolve_resub),
                       post_id: int = Path(...)) -> Post:
    """ Resolve the post from the path parameter. """
    pass


async def resolve_user_owned_post(post: Post = Depends(resolve_post),
                                  current_user: User = Depends(get_current_user)) -> Post:
    """ Verify that the authorized user owns the post before returning. """
    pass


async def resolve_post_for_post_owner_or_resub_owner(resub: Resub = Depends(resolve_resub),
                                                     post: Post = Depends(resolve_post),
                                                     current_user: User = Depends(get_current_user)) -> Post:
    """ Verify that the authorized user owns the post or owns the resub before returning. """
    pass

