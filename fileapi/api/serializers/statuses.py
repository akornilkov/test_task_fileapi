from fileapi.app.marshmallow import ma
from marshmallow import fields


class StatusSchema(ma.Schema):
    id = fields.Integer()
    uuid = fields.String()
    name = fields.String()
    name_en = fields.String()
    description = fields.String()


# init Schema
status_schema = StatusSchema()
statuses_schema = StatusSchema(many=True)
