"""
Employee-related blueprint/views.
"""
from flask import Blueprint

from app.controllers.employees import EmployeeController, EmployeeControllerException
from app.errors import create_error_response


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
    controller = EmployeeController()
    try:
        report = controller.generate_report()
    except EmployeeControllerException as err:
        return create_error_response({'message': str(err)}, 400)

    return report
