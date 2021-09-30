"""
Test module for the EmployeeController.
"""
import datetime
import pytest

from werkzeug.datastructures import FileStorage

from app.controllers.employees import EmployeeController, EmployeeControllerException
from app.models.employees import Employee, EmployeeWorkReport, EmployeeWorkUnit

from tests import BaseTestController


class TestBaseVerifiedUserController(BaseTestController):
    """
    Test encapsulator for EmployeeController.
    """
    def _clean_db_queries(self):
        """ Queries for cleaning the db at class teardown """
        self.session.query(Employee).delete()
        self.session.query(EmployeeWorkReport).delete()
        self.session.query(EmployeeWorkUnit).delete()

    def _get_controller(self):
        """ Returns an instance of EmployeeController """
        return EmployeeController(db_session=self.session)

    def test_constructor(self):
        """ Default test case for class constructor """
        assert self._get_controller().db_session == self.session

    @pytest.mark.parametrize('filename, expected_id', [
        ('time-report-42.csv', 42),
        ('time-report-58.abc', 58),
    ])
    def test__resolve_report_id(self, filename, expected_id):
        """ Default test case for EmployeeController::_resolve_report_id """
        source = FileStorage(b'', filename)
        assert self._get_controller()._resolve_report_id(source) == expected_id

    @pytest.mark.parametrize('filename', [
        'time-report-42-41.csv',
        'report-time-42.csv',
        'random.name',
    ])
    def test__recover_report_id_fails(self, filename):
        """ Test case for EmployeeController::_recover_report_id when the filename does not meet expectations """
        source = FileStorage(b'', filename)
        with pytest.raises(EmployeeControllerException):
            self._get_controller()._resolve_report_id(source)

    @pytest.mark.parametrize('date, expected_result', [
        (
            datetime.date(2021, 8, 5),
            {'startDate': '2021-08-01', 'endDate': '2021-08-15'},
        ),
        (
            datetime.date(2021, 2, 18),
            {'startDate': '2021-02-16', 'endDate': '2021-02-28'},
        ),
        (
            datetime.date(2021, 12, 31),
            {'startDate': '2021-12-16', 'endDate': '2021-12-31'},
        ),
    ])
    def test__get_period(self, date, expected_result):
        """ Default test case for EmployeeController::_get_period """
        assert self._get_controller()._get_period(date) == expected_result
