"""
Database setup.
"""
from flask import current_app, Flask, g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

from app.config import Config


DATABASE = SQLAlchemy()


def get_db_uri():
    """
    Resolves the database connection string.

    Returns:
        - (str): Connection string.
    """
    if Config.DEBUG:
        return 'sqlite:///../local.db'

    dbc = Config.Database
    return f'postgresql://{dbc.USER}:{dbc.PASS}@{dbc.HOST}:{dbc.PORT}/{dbc.NAME}'


def add_db_to_app_context():
    """
    Sets the database to the application context g.
    """
    g.db = DATABASE


def database_setup(app: Flask):
    """
    Sets up the database for the application.

    Args:
        - app (Flask): Current application instance.
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DATABASE.init_app(app)
    with app.app_context():
        # Putting this block into a try/catch to avoid using alembic to perform DB migrations for now
        try:
            DATABASE.create_all()
        except Exception:
            pass
    app.before_request(add_db_to_app_context)
