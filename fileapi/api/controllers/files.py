import uuid
from pprint import pprint

from fileapi.api.models.files import FileModel

from fileapi.app.db import get_objects, create_object, update_objects
from fileapi.app.ext.exceptions import DatabaseError


def get_files(filter_by: dict):
    return get_objects(FileModel, filter_by)


def get_files_by_task_id(task_id):
    return get_files({'task_id': task_id})


def get_files_by_date_created(date):
    return get_files({'date_created': date})


def get_file_by_uuid(uuid4):
    return get_objects(FileModel, {'uuid': uuid4}, 1)


def create_file(file: dict):
    pprint(file)
    if not file.get('task_id', None):
        raise DatabaseError('task_id is None for file creation')
    new_file = FileModel(
        uuid=uuid.uuid4(),
        name=file.get('name', ''),
        size=file.get('size', ''),
        description=file.get('description', ''),
        task_id=file.get('task_id'),
        started_at=file.get('started_at', None),
        finished_at=file.get('finished_at', None),
        loaded_from=file.get('url', None),
        loaded_to=file.get('path', None),
    )
    create_object(new_file)
    return new_file


def update_file(file: dict, filter_by: dict = None):
    updated_file = update_objects(FileModel, filter_by, file)
    return updated_file
