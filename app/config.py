"""
Simple config module.
"""
import os

from app.constants import config as config_constants


class Config:
    LOG_LEVEL = os.getenv('LOG_LEVEL', config_constants.Defaults.LOG_LEVEL)
    ENVIRONMENT = os.getenv('ENVIRONMENT', config_constants.Defaults.ENVIRONMENT)
    SECRET_KEY = os.getenv('SECRET_KEY', config_constants.Defaults.SECRET_KEY)
    DEBUG = ENVIRONMENT != config_constants.Environments.PRODUCTION

    class Database:
        HOST = os.getenv('DB_HOST', config_constants.Defaults.DB.HOST)
        PORT = os.getenv('DB_PORT', config_constants.Defaults.DB.PORT)
        NAME = os.getenv('DB_NAME', config_constants.Defaults.DB.NAME)
        USER = os.getenv('DB_USER', config_constants.Defaults.DB.USER)
        PASS = os.getenv('DB_PASS', config_constants.Defaults.DB.PASS)
