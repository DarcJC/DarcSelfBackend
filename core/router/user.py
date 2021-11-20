from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel, constr, HttpUrl
from starlette.responses import Response

from core.controller import user
from core.dependency.oauth import get_current_user
from storage.tortoise.models import WechatUser, WechatUserRealname

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


class WechatProfileUpdateRequest(BaseModel):
    nickname: constr(min_length=1)
    avatar_url: HttpUrl


@router.patch(
    '/wechat/profile',
    description="Updating profile",
    status_code=204,
)
async def wechat_update_profile(
        data: WechatProfileUpdateRequest,
        current_user: WechatUser = Depends(get_current_user),
):
    await user.wechat_profile_update(current_user, data.nickname, data.avatar_url)
    return Response(status_code=204)


@router.patch(
    '/wechat/realname',
    description="Updating realname",
    status_code=204,
)
async def wechat_set_realname(
        res: WechatUserRealname = Depends(user.set_realname),
):
    return Response(status_code=204)
