import json
from datetime import timedelta
from typing import Optional

import aiohttp
from fastapi import HTTPException
from pydantic import BaseModel, parse_obj_as

from configuration import setting
from storage.redis import redis

_MINIPROGRAM_AT_PARAM = dict(
    grant_type="client_credential",
    appid=setting.WECHAT_APPID,
    secret=setting.ADMIN_SECRET,
)
_MINIPROGRAM_AT_CACHE_KEY = 'c_miniprogram_access_token'


async def get_miniprogram_access_token() -> str:
    cached = await redis.get(_MINIPROGRAM_AT_CACHE_KEY)
    if not cached or type(cached) is not str:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.weixin.qq.com/cgi-bin/token', params=_MINIPROGRAM_AT_PARAM) as resp:
                data = await resp.json()
                if data.get('errcode', -1):
                    raise HTTPException(500, {
                        "msg": "Could not fetch access token from wechat server",
                    })
                cached = data['access_token']
    await redis.set(_MINIPROGRAM_AT_CACHE_KEY, cached, ex=timedelta(seconds=3600))
    return cached


class Code2SessionSchema(BaseModel):
    openid: Optional[str] = None
    session_key: Optional[str] = None
    unionid: Optional[str] = None
    errcode: Optional[int] = 0
    errmsg: Optional[str] = None


async def code2session(code: str) -> Code2SessionSchema:
    param = dict(
        appid=setting.WECHAT_APPID,
        secret=setting.WECHAT_SECRET,
        js_code=code,
        grant_type='authorization_code',
    )
    async with aiohttp.request('GET', 'https://api.weixin.qq.com/sns/jscode2session', params=param) as resp:
        return parse_obj_as(Code2SessionSchema, json.loads(await resp.text()))
