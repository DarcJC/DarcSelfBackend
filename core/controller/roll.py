import uuid
from typing import List

from storage.tortoise import WechatUserSchema
from storage.tortoise.models import WechatUser, Rolling


async def create_rolling(title: str, owner: WechatUser) -> Rolling:
    return await Rolling.create(title=title, owner=owner)


async def rolling_add_participant(rid: uuid.UUID, user: WechatUser) -> None:
    roll = await Rolling.get(id=rid)
    await roll.joiner.add(user)


async def rolling_list_participant(rid: uuid.UUID) -> List[WechatUserSchema]:
    roll = await Rolling.get(id=rid)
    return [await WechatUserSchema.from_tortoise_orm(u) for u in (await roll.joiner.all())]
