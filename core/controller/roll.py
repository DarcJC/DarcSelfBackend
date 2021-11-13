import uuid

from storage.tortoise.models import WechatUser, Rolling


async def create_rolling(title: str, owner: WechatUser) -> Rolling:
    return await Rolling.create(title=title, owner=owner)


async def rolling_add_participant(rid: uuid.UUID, user: WechatUser) -> None:
    roll = await Rolling.get(id=rid)
    await roll.joiner.add(user)
