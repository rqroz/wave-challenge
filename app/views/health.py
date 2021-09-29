"""
Health blueprint to represent app state.
"""
import os
import datetime

from flask import Blueprint, jsonify


BLUEPRINT = Blueprint('health', __name__, url_prefix='/health')


@BLUEPRINT.route('', methods=['GET'])
def process_employees_csv():
    """
    Processes CSV file with employee information.
    """
    return jsonify({
        'status': 'ok',
        'host': os.getenv('HOSTNAME'),
        'timestamp': datetime.datetime.now().timestamp(),
    })
