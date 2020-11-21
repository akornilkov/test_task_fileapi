from typing import List

import yaml
import os
from dataclasses import dataclass

ENVIRONMENT = os.environ.get('ENVIRONMENT', 'LOCAL').upper()
CONFIG_FILE = os.environ.get('CONFIG_FILE', f'./config/{ENVIRONMENT.lower()}.yml')

README_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    'README.md'
)


class Environment:
    LOCAL = 'LOCAL'
    TESTING = 'TESTING'
    TEST = 'TEST'
    DEV = 'DEV'
    PROD = 'PROD'


@dataclass
class BaseConfig:
    APP_NAME: str
    LOG_LEVEL: str
    README_PATH = README_PATH

    CELERY_BROKER_URL: str

    TASK_MAX_RETRIES: int
    TASK_DELAY: int

    FILES_BASE_PATH: str
    FILE_CHUNKS_COUNT: int

    DB_PG_NAME: str
    DB_SCHEMA: str
    DB_PG_USERNAME: str
    DB_PG_PASSWORD: str
    DB_PG_HOST: str
    DB_PG_PORT: int = 5432
    INIT_LOGGING: bool = True

    STATUSES = [
        {'name': 'Создана', 'name_en': 'CREATED', 'description': 'Задача создана'},
        {'name': 'Обрабатывается', 'name_en': 'PENDING', 'description': 'Задача обрабатывается'},
        {'name': 'Завершена', 'name_en': 'CLOSED', 'description': 'Задача успешно завершена'},
        {'name': 'Просрочена', 'name_en': 'OVERDUE', 'description': 'Задача просрочена'},
    ]

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = True

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return 'postgresql://{user}:{password}@{host}:{port}/{db_name}'.format(
            user=self.DB_PG_USERNAME,
            password=self.DB_PG_PASSWORD,
            host=self.DB_PG_HOST,
            port=self.DB_PG_PORT,
            db_name=self.DB_PG_NAME,
        )

    @property
    def ENVIRONMENT(self):
        return str(ENVIRONMENT).upper()


class LocalConfig(BaseConfig):
    pass


class DevConfig(BaseConfig):
    pass


class TestConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


class ProdConfig(BaseConfig):
    pass


def get_env_name():
    return os.environ.get('ENVIRONMENT', 'LOCAL').lower()


def load_config_by_env(environment_name: str):
    with open(f'config/{environment_name}.yaml') as f:
        return yaml.safe_load(f)


def get_config():
    env_name = get_env_name()
    source_data_config = load_config_by_env(env_name)
    return {
        'local': LocalConfig,
        'dev': DevConfig,
        'test': TestConfig,
        'testing': TestingConfig,
        'prod': ProdConfig
    }[env_name](**source_data_config)


config = get_config()
