from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from configuration import setting
from core.router import router_list


class ASGIBuilder(object):
    def __init__(self):
        self._app = FastAPI(
            title='DarcSelf Backend API',
            description='Powered by magic DarcJC',
            version='0.1.0',
        )

    def apply_routes(self):
        for i in router_list:
            self._app.include_router(i)

    def apply_tortoise(self):
        register_tortoise(
            self._app, db_url=setting.POSTGRES_DSN,
            modules={
                'models': ['storage.tortoise.models'],
            },
            generate_schemas=True,
            add_exception_handlers=True,
        )

        @self._app.on_event('shutdown')
        async def shutdown():
            await Tortoise.close_connections()

    def build(self):
        self.apply_routes()
        self.apply_tortoise()
        return self._app


app = ASGIBuilder().build()

__all__ = ('app', )
