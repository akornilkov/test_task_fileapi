import os
from pprint import pprint

from flask import jsonify, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
from pathlib import Path

from fileapi.api.v1.blueprint import v1_blueprint
from fileapi.api.controllers import files
from fileapi.api.controllers import filemanager
from fileapi.api.controllers.common import make_public_url
from fileapi.api.serializers.files import (
    file_schema,
    files_schema,
)
from fileapi.app.cache import cached
from fileapi.app.config import config


@v1_blueprint.route('/files', methods=['GET'])
@cached(timeout=5)
def get_all_files():
    result = files.get_files({})
    schema_multi = files_schema.dump(result)
    return jsonify([make_public_url(item, 'v1.get_file_info_by_uuid') for item in schema_multi])


@v1_blueprint.route('/files', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and filemanager.allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(config.UPLOAD_FOLDER, filename))
        return jsonify({"RESULT": filename})
    return jsonify({"RESULT": "NOT OK"})


@v1_blueprint.route('/files/<uuid>', methods=['PUT'])
def update_file(uuid):
    result = files.update_files(request.json, {'uuid': uuid})
    schema = file_schema.dump(result)
    return jsonify(make_public_url(schema, 'v1.get_file_by_uuid'))


@v1_blueprint.route('/files/<uuid>', methods=['DELETE'])
def delete_file(uuid):
    pprint(files.delete_files({'uuid': uuid}))
    return '', 204


@v1_blueprint.route('/files/<uuid>/info', methods=['GET'])
@cached(timeout=5)
def get_file_info_by_uuid(uuid):
    result = files.get_file_by_uuid(uuid)
    schema = file_schema.dump(result)
    return jsonify(make_public_url(schema, 'v1.get_file_data_by_uuid'))


@v1_blueprint.route('/files/<uuid>/data', methods=['GET'])
def get_file_data_by_uuid(uuid):
    result = files.get_file_by_uuid(uuid)
    schema = file_schema.dump(result)
    path, name = filemanager.split_path(schema.get('loaded_to'))
    return send_from_directory(path, name)
