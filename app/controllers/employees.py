"""
Employee-related controller module.
"""
from flask import g

from app.models.employees import Employee, EmployeeWorkUnit


class EmployeeControllerException(Exception):
    """ Exception class used by the EmployeeController to identify controller-specific errors """
    pass


class EmployeeController(object):
    """
    Controller to encapsulate employee-related data/logic manipulations.
    """
    def __init__(self, db_session=None):
        if not db_session:
            db_session = g.db.session
        self.db_session = db_session

    def generate_report(self):
        return {'blah': [e.serialize() for e in Employee.query.all()]}
