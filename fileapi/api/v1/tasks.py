from flask import jsonify, request
from fileapi.api.v1.blueprint import v1_blueprint
from fileapi.api.controllers import tasks
from fileapi.api.controllers.common import make_public_url
from fileapi.api.serializers.tasks import (
    task_schema,
    tasks_schema,
)
from fileapi.api.serializers.statuses import (
    status_schema,
)
from fileapi.app.cache import cached
from fileapi.api.tasks.web import handle_download_files


@v1_blueprint.route('/tasks', methods=['GET'])
@cached(timeout=5)
def get_all_tasks():
    result = tasks.get_tasks({})
    schema_multi = tasks_schema.dump(result)
    return jsonify([make_public_url(item, 'v1.get_task_by_uuid') for item in schema_multi])


@v1_blueprint.route('/tasks', methods=['POST'])
def create_task():
    files = request.json.pop('files', [])
    result = tasks.create_task(request.json)
    schema = task_schema.dump(result)
    urls = [file.get('load_from', '') for file in files]
    handle_download_files.apply_async(args=[urls, schema.get('id')])
    return jsonify(make_public_url(schema, 'v1.get_task_by_uuid'))


@v1_blueprint.route('/tasks/<uuid>', methods=['PUT'])
def update_task(uuid):
    result = tasks.update_tasks(request.json, {'uuid': uuid})
    schema = task_schema.dump(result)
    return jsonify(make_public_url(schema, 'v1.get_task_by_uuid'))


@v1_blueprint.route('/tasks/<uuid>', methods=['DELETE'])
def delete_task(uuid):
    tasks.delete_tasks({'uuid': uuid})
    return '', 204


@v1_blueprint.route('/tasks/<uuid>', methods=['GET'])
@cached(timeout=5)
def get_task_by_uuid(uuid):
    result = tasks.get_task_by_uuid(uuid)
    schema = task_schema.dump(result)
    return jsonify(make_public_url(schema, 'v1.get_task_by_uuid'))


@v1_blueprint.route('/tasks/<uuid>/status', methods=['GET'])
def get_task_status_by_task_uuid(uuid):
    result = tasks.get_task_status_by_task_uuid(uuid)
    schema = status_schema.dump(result)
    return jsonify(schema)
