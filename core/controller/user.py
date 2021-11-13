from fastapi import HTTPException

from core.controller.wechat import code2session
from storage.tortoise.models.user import WechatUser


async def wechat_login(code: str) -> str:
    data = await code2session(code)
    if data.errcode == 0:
        user, created = await WechatUser.get_or_create(openid=data.openid)
        user.session_key = data.session_key
        await user.save()
        return (await user.new_token()).token
    raise HTTPException(401, dict(msg='Bad code'))

