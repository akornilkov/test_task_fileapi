from fileapi.app.marshmallow import ma
from marshmallow import fields

from .files import FileSchema


class TaskSchema(ma.Schema):
    id = fields.Integer()
    uuid = fields.String()
    name = fields.String()
    description = fields.String()
    created_at = fields.DateTime()
    started_at = fields.DateTime()
    finished_at = fields.DateTime()
    expires_at = fields.DateTime()
    status_id = fields.Integer()
    files = fields.Nested(FileSchema, many=True)


# init Schema
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
