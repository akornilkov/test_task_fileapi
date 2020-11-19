from flask_sqlalchemy import SQLAlchemy
import logging

from sqlalchemy.orm.exc import NoResultFound

from fileapi.app.config import config

from fileapi.app.ext.exceptions import (
    DatabaseError,
    get_classname,
)

# INIT DB
db = SQLAlchemy()

logger = logging.getLogger(config.APP_NAME)


def get_objects(models, filter_by: dict, limit: int = None, offset: int = None):
    objects = db.session.query(models).filter_by(**filter_by)
    try:
        if not limit and not offset:
            return objects.all()
        else:
            if limit == 1:
                if not offset:
                    return objects.one()
                else:
                    return objects.offset(offset).one()
            else:
                if not offset:
                    return objects.limit(limit).all()
                else:
                    return objects.limit(limit).offset(offset).all()
    except NoResultFound as e:
        logger.exception(e)
        raise DatabaseError(message=f'Object {get_classname(models)} not found by'
                                    f' filter:{filter_by.__str__()} limit={limit} offset={offset}')
    except Exception as e:
        logger.exception(e)
        raise DatabaseError(e)


def create_object(obj):
    try:
        result = db.session.add(obj)
        db.session.commit()
        return result
    except Exception as e:
        logger.exception(e)
        raise DatabaseError(e)


def create_objects(objects):
    try:
        result = db.session.bulk_save_objects(objects)
        db.session.commit()
        return result
    except Exception as e:
        logger.exception(e)
        raise DatabaseError(e)


def update_objects(model, filter_by: dict, data: dict):
    try:
        objects = db.session.query(model).filter_by(**filter_by)
        count = objects.update(data)
        db.session.commit()
        if count:
            if count == 1:
                return objects.one()
            else:
                return objects.all()
        else:
            raise Exception(f'Object {get_classname(model)} not found by'
                            f' filter:{filter_by.__str__()}')
    except Exception as e:
        logger.exception(e)
        raise DatabaseError(e)


def delete_objects(model, filter_by: dict):
    try:
        objects = db.session.query(model).filter_by(**filter_by)
        count = objects.delete()
        db.session.commit()
        if count:
            return count
        else:
            raise Exception(f'Object {get_classname(model)} not found by'
                            f' filter:{filter_by.__str__()}')
    except Exception as e:
        logger.exception(e)
        raise DatabaseError(e)
