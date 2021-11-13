from fastapi import APIRouter, Depends

from core.dependency.oauth import get_current_user
from storage.tortoise.models import WechatUser

router = APIRouter(tags=['Roll'], prefix='/roll')


@router.post('/new')
def new_roll(
        user: WechatUser = Depends(get_current_user),
):
    pass
