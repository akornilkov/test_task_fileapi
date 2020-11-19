from flask import jsonify
from fileapi.api.v1.blueprint import v1_blueprint


@v1_blueprint.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': '1'})
