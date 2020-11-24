import uuid
from typing import List

import flask

from fileapi.api import v1
from . import logging
from .db import db
from .ext.exceptions import (
    DatabaseError,
)
from .ext.error_handlers import (
    database_error_handler,
)
from .marshmallow import ma
from .cache import cache
from fileapi.api.models import *
from fileapi.app.config import config
from fileapi.api.tasks.celery import celeryApp
from fileapi.api.controllers.filemanager import create_dir_if_not_exists


def create_app(extra_config: dict = None):
    if config.INIT_LOGGING:
        logging.init_logging()
    create_dir_if_not_exists(config.FILES_BASE_PATH)
    create_dir_if_not_exists(config.UPLOAD_FOLDER)
    app = flask.Flask(config.APP_NAME)
    app.config.from_object(config)
    app.config.update(CELERY_BROKER_URL='redis://localhost:6379/0')
    app.app_context().push()
    db.init_app(app)
    ma.init_app(app)
    celeryApp.init_app(app)
    cache.init_app(app, config={'CACHE_TYPE': 'simple'})

    if extra_config:
        if extra_config.pop('migrate', False):
            db.drop_all()
            db.create_all()
            for status in create_statuses(config.STATUSES):
                db.session.add(status)
            db.session.commit()
        app.config.from_mapping(extra_config)

    app.url_map.strict_slashes = False

    app.register_blueprint(v1.blueprint, url_prefix='/v1')
    app.register_error_handler(DatabaseError, database_error_handler)
    app.add_url_rule('/health', 'health', lambda: flask.jsonify({'status': 'ok'}))

    return app


def create_statuses(raw: List[dict]):
    for status in [
        StatusModel(
            uuid=uuid.uuid4(),
            name=item.get('name'),
            name_en=item.get('name_en'),
            description=item.get('description'),
        )
        for item in raw
    ]:
        yield status
