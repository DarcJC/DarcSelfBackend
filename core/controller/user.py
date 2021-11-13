from fastapi import HTTPException
from pydantic import HttpUrl

from core.controller.wechat import code2session
from storage.tortoise.models.user import WechatUser, WechatUserProfile


async def wechat_login(code: str) -> str:
    data = await code2session(code)
    if data.errcode == 0:
        user, created = await WechatUser.get_or_create(openid=data.openid)
        user.session_key = data.session_key
        await user.save()
        return (await user.new_token()).token
    raise HTTPException(401, dict(msg='Bad code'))


async def wechat_profile_update(user: WechatUser, nickname: str, avatar_url: HttpUrl) -> None:
    profile, created = await WechatUserProfile.get_or_create(owner=user)
    profile.nickname = nickname
    profile.avatar = avatar_url
    await profile.save()
