"""
Register blueprints defined in app/views/* into the server app.
"""
from flask import Flask

from app.views import employees
from app.views import health


def views_setup(app: Flask):
    """
    Setup all of the views for the application.
    """
    app.register_blueprint(health.BLUEPRINT)
    app.register_blueprint(employees.BLUEPRINT)
