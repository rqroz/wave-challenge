"""
Config-level constants.
"""


class Environments:
    PRODUCTION = 'prod'
    DEVELOPMENT = 'dev'


class Defaults:
    ENVIRONMENT = Environments.DEVELOPMENT
    LOG_LEVEL = 'DEBUG'

    class DB:
        HOST = 'localhost'
        PORT = '5432'
        NAME = 'wavedb'
        USER = 'test'
        PASS = 'test'
