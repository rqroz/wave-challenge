"""
Global error handlers module.
"""
from flask import Flask, jsonify, Response
from structlog import get_logger
from typing import Dict


def create_error_response(data: Dict[str, str], status_code: int) -> Response:
    """
    Builds proper response for error handlers.

    Args:
        - data (Dict[str, str]): Map of meaningful information to send back to the client;
        - status_code (int): Desired status code to set in the response.

    Returns:
        - resp (flask.Response): Response object created from arguments.
    """
    resp = jsonify(data)
    resp.status_code = status_code
    return resp


def errors_setup(app: Flask):
    """
    Adds error views to nicely handle common exceptions.

    Args:
        - app (Flask): Application to attach error views.
    """
    @app.errorhandler(500)
    def error_handler_500(error):
        return create_error_response({'message': str(error)}, 500)

    @app.errorhandler(404)
    def error_handler_404(_):
        return create_error_response({'message': 'Not found'}, 404)

    @app.errorhandler(405)
    def error_handler_405(_):
        return create_error_response({'message': 'Method not allowed on resource uri'}, 405)

    @app.errorhandler(400)
    def error_handler_400(error):
        return create_error_response({'message': error}, 400)
