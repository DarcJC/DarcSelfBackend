from tortoise import Model, fields


class Rolling(Model):
    id = fields.UUIDField(pk=True, description="Internal Rolling ID")
    title = fields.CharField(max_length=256, default="", description="Title of the rolling")
    joiner = fields.ManyToManyField('models.WechatUser', related_name='joined_rolls')
    owner: fields.ForeignKeyRelation = fields.ForeignKeyField('models.WechatUser', 'owned_rolls')
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
