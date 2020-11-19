from flask import jsonify, request
from fileapi.api.v1.blueprint import v1_blueprint
from fileapi.api.controllers import tasks
from fileapi.api.controllers.common import make_public_url
from fileapi.api.serializers.tasks import (
    task_schema,
    tasks_schema,
)
from fileapi.app.cache import cached


@v1_blueprint.route('/tasks', methods=['GET'])
@cached(timeout=5)
def get_all_tasks():
    result = tasks.get_tasks({})
    schema_multi = tasks_schema.dump(result)
    return jsonify([make_public_url(item, 'v1.get_task_by_uuid') for item in schema_multi])


@v1_blueprint.route('/tasks', methods=['POST'])
def create_task():
    result = tasks.create_task(request.json)
    schema = task_schema.dump(result)
    return jsonify(make_public_url(schema, 'v1.get_task_by_uuid'))


@v1_blueprint.route('/statuses/<uuid>', methods=['PUT'])
def update_task(uuid):
    result = tasks.update_tasks(request.json, {'uuid': uuid})
    schema = task_schema.dump(result)
    return jsonify(make_public_url(schema, 'v1.get_task_by_uuid'))


@v1_blueprint.route('/tasks/<uuid>', methods=['DELETE'])
def delete_task(uuid):
    tasks.delete_tasks({'uuid': uuid})
    return '', 204


@v1_blueprint.route('/tasks/<uuid>', methods=['GET'])
@cached(timeout=60)
def get_task_by_uuid(uuid):
    result = tasks.get_task_by_uuid(uuid)
    schema = task_schema.dump(result)
    return jsonify(make_public_url(schema, 'v1.get_task_by_uuid'))
