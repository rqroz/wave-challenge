"""
Config-level constants.
"""


class Environments:
    PRODUCTION = 'prod'
    DEVELOPMENT = 'dev'
    TESTING = 'test'


class Defaults:
    ENVIRONMENT = Environments.DEVELOPMENT
    LOG_LEVEL = 'DEBUG'
    SECRET_KEY = 'dummy-secret'

    class DB:
        HOST = 'localhost'
        PORT = '5432'
        NAME = 'wavedb'
        USER = 'test'
        PASS = 'test'
