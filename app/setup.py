import os
import json
import structlog

from flask import Flask

from app.logging import logging_setup
from app.errors import errors_setup
from app.blueprints import views_setup


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'sqlite'),
    )
    logging_setup()
    errors_setup(app)
    views_setup(app)

    @app.after_request
    def log_access(response):
        data = '<not printable>'
        if response.headers.get('Content-Type') == 'application/json':
            try:
                data = response.get_data().decode('utf-8')
            except UnicodeDecodeError:
                pass

        try:
            log_message = json.loads(data)
        except json.JSONDecodeError:
            log_message = data
        structlog.get_logger('access').info('RESPONSE', status=response.status_code, data=log_message)
        return response

    return app
