from fileapi.app.marshmallow import ma
from marshmallow import fields


class StatusSchema(ma.Schema):
    id = fields.Integer(attribute='id')
    uuid = fields.String(attribute='uuid')
    name = fields.String(attribute='name')
    name_en = fields.String(attribute='name_en')
    description = fields.String(attribute='description')


# init Schema
status_schema = StatusSchema()
statuses_schema = StatusSchema(many=True)
