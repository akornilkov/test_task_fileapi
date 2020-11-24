import uuid

from fileapi.api.models.statuses import StatusModel

from fileapi.app.db import get_objects, create_object, update_objects, delete_objects


def get_statuses(filter_by: dict):
    return get_objects(StatusModel, filter_by)


def get_status_by_uuid(uuid4: str):
    return get_objects(StatusModel, {'uuid': uuid4}, 1)


def get_status_by_id(status_id: int):
    return get_objects(StatusModel, {'id': status_id}, 1)


def create_status(status: dict):
    new_status = StatusModel(
        uuid=uuid.uuid4(),
        name=status.get('name', ''),
        name_en=status.get('name_en', ''),
        description=status.get('description', ''),
    )
    create_object(new_status)
    return new_status


def update_status(status: dict, filter_by: dict = None):
    updated_status = update_objects(StatusModel, filter_by, status)
    return updated_status


def delete_statuses(filter_by: dict = None):
    return delete_objects(StatusModel, filter_by)
