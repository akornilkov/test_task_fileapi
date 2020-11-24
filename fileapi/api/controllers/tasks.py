import uuid
from typing import List, Union

from fileapi.api.models.tasks import TaskModel
from fileapi.api.models.statuses import StatusModel
from fileapi.app.db import (
    get_objects,
    create_object,
    update_objects,
    delete_objects,
)
from fileapi.api.controllers.statuses import (
    get_status_by_id,
)


def get_tasks(filter_by: dict):
    return get_objects(TaskModel, filter_by)


def get_task_by_uuid(uuid4) -> TaskModel:
    return get_objects(TaskModel, {'uuid': uuid4}, 1)


def get_tasks_by_date_created(date) -> List[TaskModel]:
    return get_tasks({'date_created': date})


def get_tasks_by_status_id(status_id) -> List[TaskModel]:
    return get_tasks({'status_id': status_id})


def create_task(task: dict) -> TaskModel:
    new_task = TaskModel(
        uuid=uuid.uuid4(),
        name=task.get('name', ''),
        description=task.get('description', ''),
    )
    create_object(new_task)
    return new_task


def update_tasks(task: dict, filter_by: dict = None) -> Union[TaskModel, List[TaskModel]]:
    updated_task = update_objects(TaskModel, filter_by, task)
    return updated_task


def delete_tasks(filter_by: dict = None):
    return delete_objects(TaskModel, filter_by)


def get_task_status_by_task_uuid(uuid4: str) -> Union[StatusModel, None]:
    if task := get_task_by_uuid(uuid4=uuid4):
        return get_status_by_id(task.status_id)
    else:
        return None
