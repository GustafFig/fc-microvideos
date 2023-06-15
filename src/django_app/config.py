import os
from pathlib import Path
from typing import Dict, List

import dj_database_url
from pydantic import BaseSettings, Field, config, validator

_ENV_FOLDER = Path(__file__).resolve().parent.parent.parent / 'envs'
APP_ENV = os.getenv('APP_ENV')
_LIST_TYPE_VARIABLES = (
    'installed_apps',
    'middlewares_additional'
)

class ConfigService(BaseSettings):

    database_dsn: str
    database_conn: Dict = Field(init=False, default=None)
    language_code = 'en-us'
    debug: bool = False
    installed_apps: List[str]
    middlewares_additional: List[str]
    secret_key: str

    class Config(config.BaseConfig):
        env_file = f"{_ENV_FOLDER}/.env", f"{_ENV_FOLDER}/.env.{APP_ENV}"

        @classmethod
        def parse_env_var(cls, field_name, raw_value: str):
            if field_name in _LIST_TYPE_VARIABLES:
                return [app.strip() for app in raw_value.splitlines() if app.strip() != '']
            return cls.json_loads(raw_value)

    @validator('database_conn', pre=True)
    def make_database_conn(cls, v, values, **kwargs):  # pylint: disable=no-self-argument,unused-argument
        return dj_database_url.config(default=values['database_dsn'])


config_service = ConfigService()
