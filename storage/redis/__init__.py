import aioredis

from configuration import setting


class RedisBuilder(object):
    def __init__(self, redis_dsn):
        self.redis_dsn = redis_dsn
        self.single_connection = None
        self.connection_pool = None

    def create_connection_pool(self):
        self.connection_pool = aioredis.ConnectionPool().from_url(self.redis_dsn)

    def build(self) -> aioredis.Redis:
        self.create_connection_pool()
        return aioredis.Redis(connection_pool=self.connection_pool)


redis: aioredis.Redis = RedisBuilder(setting.REDIS_DSN).build()


__all__ = ('redis', )

