import random
import string
from datetime import datetime, timedelta

from tortoise import fields, Model


class WechatUser(Model):
    id = fields.IntField(pk=True, description="Internal User ID")
    openid = fields.CharField(max_length=128, description="User unique ID provided by Wechat")
    session_key = fields.CharField(
        max_length=128,
        default="",
        description="Key used to decode some information from Wechat(no vaild guarantee)"
    )
    tokens: fields.ReverseRelation['WechatUserToken']
    admin = fields.BooleanField(default=False, description="Is this user admin")
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    async def new_token(self) -> 'WechatUserToken':
        token = ''.join(random.choices(string.hexdigits, k=128))
        wut = await WechatUserToken.create(owner=self, token=token)
        return wut

    async def trim_token(self) -> None:
        # TODO implemention
        pass


class WechatUserToken(Model):
    id = fields.BigIntField(pk=True, description="Internal Token ID")
    owner: fields.ForeignKeyRelation[WechatUser] = fields.ForeignKeyField('models.WechatUser', 'tokens')
    token = fields.CharField(max_length=256, description="User Token")
    created_at = fields.DatetimeField(auto_now_add=True, description="Create Datetime")
    status = fields.BooleanField(default=True, description="To let token invaild by human operation")

    @property
    def is_vaild(self) -> bool:
        return self.status and datetime.now(self.created_at.tzinfo) - self.created_at < timedelta(days=1)