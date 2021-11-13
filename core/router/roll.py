import uuid

from fastapi import APIRouter, Depends
from starlette.responses import Response

from core.dependency.oauth import get_current_user
from storage.tortoise import RollingSchema
from storage.tortoise.models import WechatUser
from core.controller import roll

router = APIRouter(tags=['Roll'], prefix='/roll')


@router.post('/new', description="create a rolling", response_model=RollingSchema, status_code=201)
async def new_roll(
        title: str,
        user: WechatUser = Depends(get_current_user),
):
    return await RollingSchema.from_tortoise_orm(await roll.create_rolling(title, user))


@router.put('/{rolling_id}/join', description='Add participant to rolling')
async def roll_add_participant(
        rolling_id: uuid.UUID,
        current_user: WechatUser = Depends(get_current_user),
):
    await roll.rolling_add_participant(rolling_id, current_user)
    return Response(status_code=204)
