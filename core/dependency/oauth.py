from fastapi import HTTPException

from storage.tortoise.models import WechatUserToken


async def get_current_user(access_token: str):
    wut = await WechatUserToken.get_or_none(token=access_token)
    if wut is None or not wut.is_vaild:
        raise HTTPException(401, dict(msg='Bad token'))
    return await wut.owner
