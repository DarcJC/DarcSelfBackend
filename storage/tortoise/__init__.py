from tortoise import Tortoise, run_async

from configuration import setting


async def setup_tortoise():
    await Tortoise.init(
        db_url=setting.POSTGRES_DSN,
        modules={'models': ['storage.tortoise.models']},
    )
    await Tortoise.generate_schemas()
