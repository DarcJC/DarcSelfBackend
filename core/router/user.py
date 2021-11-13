from fastapi import APIRouter, Body
from pydantic import BaseModel

from core.controller import user

router = APIRouter(tags=['User'], prefix='/user')


class WechatLoginResponse(BaseModel):
    access_token: str


@router.post(
    '/wechat/login/{code}',
    description="Get user token via wx.login()'s code. Only 3 token available per user at same time.",
    response_model=WechatLoginResponse,
    status_code=201,
)
async def wechat_login(code: str):
    return WechatLoginResponse(access_token=await user.wechat_login(code))

