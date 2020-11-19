from fileapi.app.marshmallow import ma
from marshmallow import fields


class FileSchema(ma.Schema):
    id = fields.Integer()
    uuid = fields.String()
    name = fields.String()
    size = fields.Float()
    description = fields.String()
    task_id = fields.Integer()


# init Schema
task_schema = FileSchema()
tasks_schema = FileSchema(many=True)