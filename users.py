"""_summary_
This file consists of all methods to user route
"""


from typing import List, Union
from fastapi import APIRouter, HTTPException
from models import User

users_router = APIRouter()


@users_router.get('/')
async def get_allusers(name: Union[str, None] = None) -> List[User]:
    if name is None:
        users = await User.find_all().to_list()
        return users
    else:
        searched_results = await User.find(User.name == name).to_list()
        return searched_results


@users_router.post('/')
async def create_user(user: User):
    await user.create()
    return user
