from storage.tortoise.models import WechatUser, Rolling


async def create_rolling(title: str, owner: WechatUser) -> Rolling:
    return await Rolling.create(title=title, owner=owner)

