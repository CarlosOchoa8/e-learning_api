"""
Base settings for all apps
"""
from pydantic import Extra
from pydantic_settings import BaseSettings
import os
CONFIG_FILE = ".env"

with open('/usr/src/app/config.txt', 'r') as conf:
    lines = conf.readlines()
    for line in lines:
        if "==" in line:
            key, value = line.strip().split('==')
            os.environ[key] = value


class AppSettings(BaseSettings):
    #: The application domain
    API_DOMAIN: str = os.getenv("API_DOMAIN")

    class Config:
        env_file = CONFIG_FILE
        extra = Extra.forbid


class Settings(BaseSettings):
    #: The application domain
    API_DOMAIN: str = os.getenv("API_DOMAIN")

