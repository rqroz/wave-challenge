"""
Employee-related blueprint/views.
"""
from flask import Blueprint, request

from app.controllers.employees import EmployeeController, EmployeeControllerException
from app.errors import create_error_response


BLUEPRINT = Blueprint('employees', __name__, url_prefix='/employees')


@BLUEPRINT.route('/csv', methods=['POST'])
def process_employees_csv():
    """
    Processes a CSV file with employee information.
    """
    try:
        source = request.files['source']
    except KeyError:
        return create_error_response({'message': 'Missing source file'}, 400)

    controller = EmployeeController()
    try:
        controller.process_csv(source)
    except EmployeeControllerException as err:
        return create_error_response({'message': str(err)}, 400)

    return {'message': 'Employee work hours saved'}


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

    return {'payrollReport': {'employeeReports': report}}
