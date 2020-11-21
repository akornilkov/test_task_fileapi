import logging.config

from .config import config, Environment

LOGGING_CONFIG = {
    'version': 1,
    'filters': {},
    'formatters': {
        'console': {
            'datefmt': '%Y-%m-%d %H:%M:%S',
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'json_ensure_ascii': False,
        },
    },
    'handlers': {
        'console': {
            'level': config.LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'console',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        config.APP_NAME: {
            'level': config.LOG_LEVEL,
            'handlers': (['console']),
        },
    },
    'disable_existing_loggers': False,
}


def init_logging():
    if config.ENVIRONMENT in [
        Environment.PROD,
    ]:
        LOGGING_CONFIG['loggers'][config.APP_NAME]['handlers'].remove('console')

    logging.config.dictConfig(LOGGING_CONFIG)
