"""
Employee-related blueprint/views.
"""
from flask import Blueprint


BLUEPRINT = Blueprint('employees', __name__, url_prefix='/employees')


@BLUEPRINT.route('/csv', methods=['POST'])
def process_employees_csv():
    """
    Processes CSV file with employee information.
    """
    return {'message': 'TODO'}


@BLUEPRINT.route('/report', methods=['GET'])
def process_report():
    """
    Returns payment-related information for all employees based on time periods.
    """
    return {'message': 'TODO'}
