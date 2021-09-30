"""
Simple config module.
"""
import os

from app.constants import config as config_constants


class Config:
    LOG_LEVEL = os.getenv('LOG_LEVEL') or config_constants.Defaults.LOG_LEVEL
    ENVIRONMENT = os.getenv('ENVIRONMENT') or config_constants.Defaults.ENVIRONMENT
    SECRET_KEY = os.getenv('SECRET_KEY') or config_constants.Defaults.SECRET_KEY
    DEBUG = ENVIRONMENT != config_constants.Environments.PRODUCTION

    class Database:
        HOST = os.getenv('DB_HOST') or config_constants.Defaults.DB.HOST
        PORT = os.getenv('DB_PORT') or config_constants.Defaults.DB.PORT
        NAME = os.getenv('DB_NAME') or config_constants.Defaults.DB.NAME
        USER = os.getenv('DB_USER') or config_constants.Defaults.DB.USER
        PASS = os.getenv('DB_PASS') or config_constants.Defaults.DB.PASS
