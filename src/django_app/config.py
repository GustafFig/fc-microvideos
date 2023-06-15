import os
from pathlib import Path
from typing import Dict
from pydantic import BaseSettings, validator, Field
import dj_database_url


_ENV_FOLDER = Path(__file__).resolve().parent.parent.parent / 'envs'
APP_ENV = os.getenv('APP_ENV')


class ConfigService(BaseSettings):

    database_dsn: str
    database_conn: Dict = Field(init=False, default=None)
    language_code = 'en-us'
    debug: bool = False
    secret_key: str

    class Config:
        env_file = f"{_ENV_FOLDER}/.env", f"{_ENV_FOLDER}/.env.{APP_ENV}"

    @validator('database_conn', pre=True)
    def make_database_conn(cls, v, values, **kwargs):  # pylint: disable=no-self-argument,unused-argument
        return dj_database_url.config(default=values['database_dsn'])


config_service = ConfigService()
