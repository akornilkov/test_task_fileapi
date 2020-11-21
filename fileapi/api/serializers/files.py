from fileapi.app.marshmallow import ma
from marshmallow import fields


class FileSchema(ma.Schema):
    id = fields.Integer()
    uuid = fields.String()
    name = fields.String()
    size = fields.Integer()
    description = fields.String()
    started_at = fields.DateTime()
    finished_at = fields.DateTime()
    loaded_from = fields.String()
    loaded_to = fields.String()
    task_id = fields.Integer()


# init Schema
task_schema = FileSchema()
tasks_schema = FileSchema(many=True)
