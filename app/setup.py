"""
Application's starting point.
"""
from flask import Flask

from app.config import Config
from app.logging import logging_setup
from app.errors import errors_setup
from app.database import database_setup
from app.blueprints import views_setup

def create_app():
    """
    Creates and configures the application.

    Returns:
        - app (Flask): Application instance.
    """
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY=Config.SECRET_KEY)
    logging_setup(app)
    errors_setup(app)
    database_setup(app)
    views_setup(app)
    return app
