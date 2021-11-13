from typing import List

from fastapi import APIRouter

from core.router.manage import router as manage
from core.router.user import router as user
from core.router.roll import router as roll

router_list: List[APIRouter] = [
    manage, user, roll,
]

__all__ = ('router_list', )
