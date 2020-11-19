from fileapi.api.models.files import FileModel

from fileapi.api.controllers.common import get_objects


def get_files(filter_by: dict):
    return _get_objects(FileModel, filter_by, False)


def get_files_by_taskid(taskid):
    return get_files({'task_id': taskid})


def get_files_by_date_created(date):
    return get_files({'date_created': date})