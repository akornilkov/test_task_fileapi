import os
import math
import requests

from urllib.parse import urlparse
from datetime import datetime
from typing import List
from celery import group

from fileapi.api.tasks.celery import celeryApp
from fileapi.app.config import config
from fileapi.api.controllers.files import create_file


def chunks_offsets(parts: int, size: int):
    chunk = math.ceil(size / parts)
    return [(start, min(start + chunk - 1, size - 1))
            for start in range(0, size, chunk)]


def get_filename_from_url(url: str):
    a = urlparse(url)
    return os.path.basename(a.path)


def download_file(url, base_path):
    name = get_filename_from_url(url)
    req = requests.head(url)
    size = int(req.headers['Content-Length'])
    section_intervals = chunks_offsets(config.FILE_CHUNKS_COUNT, size)
    with open(f'{base_path}{name}', "wb") as file:
        for i, (start, end) in enumerate(section_intervals):
            headers = {"Range": "bytes=" + str(start) + "-" + str(end)}
            r = requests.get(url, headers=headers)
            file.write(r.content)
    return {
        'name': name,
        'path': f'{base_path}{name}',
        'size': size
    }


@celeryApp.task()
def one_file_handler(url, task_id):
    started_at = datetime.utcnow()
    file = download_file(url, config.FILES_BASE_PATH)
    finished_at = datetime.utcnow()
    create_file({
        'name': file.get('name', ''),
        'size': file.get('size', 0),
        'description': file.get('description', ''),
        'started_at': started_at,
        'finished_at': finished_at,
        'url': url,
        'path': file.get('path'),
        'task_id': task_id
    })


@celeryApp.task()
def handle_download_files(urls: List[str], task_id):
    print(f'Started task #{task_id} with urls {urls}')
    started_at = datetime.utcnow()
    lazy_group = group([one_file_handler.s(url, task_id) for url in urls])
    promise = lazy_group()
    promise.wait()
    ended_at = datetime.utcnow()
    print(f'Elapsed time for task #{task_id} with urls {urls}: {ended_at-started_at}')
