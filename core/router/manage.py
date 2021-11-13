import time

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import Response

from configuration import setting
from core.dependency.oauth import get_current_user
from storage.tortoise.models import WechatUser

router = APIRouter(tags=['Management'], prefix='/manage')


@router.get('/timestamp', response_model=int)
async def timestamp() -> int:
    return time.time_ns()


@router.put('/admin', status_code=204, response_model=None)
async def add_admin(secret: str, user: WechatUser = Depends(get_current_user)):
    if setting.ADMIN_SECRET is None:
        raise HTTPException(404)
    if setting.ADMIN_SECRET == secret:
        user.admin = True
        await user.save()
    return Response(status_code=204)
