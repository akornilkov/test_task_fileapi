def get_classname(cls):
    return cls.__name__


class InternalError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class DatabaseError(InternalError):
    status_code = 404

    def __init__(self, message, status_code=None, payload=None):
        super().__init__(message=f'[DBERROR]:{message}')
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
