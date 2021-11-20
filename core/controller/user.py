import random
import string
from typing import Literal, Optional

from fastapi import HTTPException, Depends
from pydantic import HttpUrl, constr, conint

from core.controller.wechat import code2session, get_wxa_code_unlimited
from storage.tortoise.models.user import WechatUser, WechatUserProfile, SceneData


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


async def create_wxa_code_unlimited(
        data: constr(max_length=512),
        page: Optional[str] = None,
        env_version: Literal['release', 'trial', 'develop'] = "release",
        width: conint(ge=280, le=1280) = 430,
        is_hyaline: bool = True,
):
    key = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
    image: bytes = await get_wxa_code_unlimited(key, page, env_version, width, is_hyaline)
    await SceneData.create(key=key, value=data)
    return image
