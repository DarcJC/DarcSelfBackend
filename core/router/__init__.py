from typing import List

from fastapi import APIRouter

from core.router.manage import router as manage
from core.router.user import router as user
from core.router.roll import router as roll
from core.router.misc import router as misc

router_list: List[APIRouter] = [
    manage, user, roll, misc,
]

__all__ = ('router_list', )
