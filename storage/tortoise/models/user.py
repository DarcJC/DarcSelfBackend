import random
import string
from datetime import datetime, timedelta

from tortoise import fields, Model

from storage.tortoise.models.roll import Rolling


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

    owned_rolls: fields.ReverseRelation['Rolling']
    joined_rolls: fields.ReverseRelation['Rolling']
    profile: fields.ReverseRelation['WechatUserProfile']
    realname: fields.ReverseRelation['WechatUserRealname']

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


class WechatUserProfile(Model):
    owner: fields.OneToOneRelation[WechatUser] = fields.OneToOneField('models.WechatUser', 'profile')
    nickname = fields.CharField(max_length=256, description="User's nickname", default="")
    avatar = fields.CharField(max_length=512, description="URL of user's avatar",
                              default="https://cdn.jsdelivr.net/gh/DarcJC/pictures-host/imgs/20211114021713.png")


class WechatUserRealname(Model):
    owner: fields.OneToOneRelation[WechatUser] = fields.OneToOneField('models.WechatUser', 'realname')
    name = fields.CharField(max_length=16, default="")


class SceneData(Model):
    id = fields.BigIntField(pk=True, description="Internal ID")
    key = fields.CharField(max_length=32, description="Key")
    value = fields.CharField(max_length=512, description="Value")
