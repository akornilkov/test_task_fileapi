from flask import jsonify, request
from fileapi.api.v1.blueprint import v1_blueprint
from fileapi.api.controllers import statuses
from fileapi.api.controllers.common import make_public_url
from fileapi.api.serializers.statuses import (
    status_schema,
    statuses_schema,
)
from fileapi.app.cache import cached


@v1_blueprint.route('/statuses', methods=['GET'])
@cached(timeout=60)
def get_all_statuses():
    result = statuses.get_statuses({})
    schema_multi = statuses_schema.dump(result)
    return jsonify([make_public_url(item, 'v1.get_status_by_uuid') for item in schema_multi])


@v1_blueprint.route('/statuses', methods=['POST'])
def create_status():
    result = statuses.create_status(request.json)
    schema = status_schema.dump(result)
    return jsonify(make_public_url(schema, 'v1.get_status_by_uuid'))


@v1_blueprint.route('/statuses/<uuid>', methods=['PUT'])
def update_status(uuid):
    result = statuses.update_status(request.json, {'uuid': uuid})
    schema = status_schema.dump(result)
    return jsonify(make_public_url(schema, 'v1.get_status_by_uuid'))


@v1_blueprint.route('/statuses/<uuid>', methods=['GET'])
@cached(timeout=60)
def get_status_by_uuid(uuid):
    result = statuses.get_status_by_uuid(uuid)
    schema = status_schema.dump(result)
    return jsonify(make_public_url(schema, 'v1.get_status_by_uuid'))
