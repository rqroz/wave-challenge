from flask import current_app, Flask, g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

from app.config import Config


DATABASE = SQLAlchemy()


def get_db_uri():
    if Config.DEBUG:
        return 'sqlite:///../local.db'

    dbc = Config.Database
    return f'postgresql://{dbc.USER}:{dbc.PASS}@{dbc.HOST}:{dbc.PORT}/{dbc.NAME}'


def add_db_to_request_context():
    g.db = DATABASE


def database_setup(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DATABASE.init_app(app)
    with app.app_context():
        DATABASE.create_all()
    app.before_request(add_db_to_request_context)
