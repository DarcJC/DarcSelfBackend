from typing import Optional, Union

from pydantic import constr, RedisDsn, BaseSettings, PostgresDsn, AnyUrl


class Settings(BaseSettings):
    ADMIN_SECRET: Optional[constr(min_length=128)]
    REDIS_DSN: Optional[RedisDsn] = 'redis://localhost:6379/0'
    WECHAT_APPID: str
    WECHAT_SECRET: str
    # 'postgres://postgres:postgres@localhost:5432/postgres'
    POSTGRES_DSN: Optional[Union[PostgresDsn, AnyUrl]] = 'sqlite://db.sqlite3'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


setting = Settings()

__all__ = ('setting', )
