from typing import List

from fastapi import APIRouter

from core.router.manage import router as manage
from core.router.user import router as user

router_list: List[APIRouter] = [
    manage, user
]

__all__ = ('router_list', )
