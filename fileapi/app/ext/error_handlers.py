from .exceptions import (
    DatabaseError,
)


def database_error_handler(e: DatabaseError):
    return e.to_dict(), 404
