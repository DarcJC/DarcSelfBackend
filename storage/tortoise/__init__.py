from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from configuration import setting
from storage.tortoise.models import Rolling


async def setup_tortoise():
    await Tortoise.init(
        db_url=setting.POSTGRES_DSN,
        modules={'models': ['storage.tortoise.models']},
    )
    await Tortoise.generate_schemas()

RollingSchema = pydantic_model_creator(Rolling)
Tortoise.init_models(["storage.tortoise.models"], "models")
