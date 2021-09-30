"""
Health blueprint to represent app state.
"""
import os
import datetime

from flask import Blueprint, jsonify


BLUEPRINT = Blueprint('health', __name__, url_prefix='/health')


@BLUEPRINT.route('', methods=['GET'])
def health_check():
    """
    Simple view to verify the server's state.
    """
    return jsonify({
        'status': 'ok',
        'host': os.getenv('HOSTNAME'),
        'timestamp': datetime.datetime.now().timestamp(),
    })
