"""
Test module for the EmployeeController.
"""
import csv
import datetime
import io
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

    @pytest.mark.parametrize('employees, work_reports, work_units, expected_result', [
        ([], [], [], []),
        (
            [
                Employee(id=1, job_group='A'),
                Employee(id=2, job_group='B'),
                Employee(id=3, job_group='B'),
            ],
            [
                EmployeeWorkReport(id=1),
            ],
            [
                EmployeeWorkUnit(
                    id=1,
                    report_id=1,
                    employee_id=1,
                    hours_worked=2.5,
                    date=datetime.date(2021, 10, 4),
                ),
                EmployeeWorkUnit(
                    id=2,
                    report_id=1,
                    employee_id=2,
                    hours_worked=2.5,
                    date=datetime.date(2021, 10, 4),
                ),
                EmployeeWorkUnit(
                    id=3,
                    report_id=1,
                    employee_id=2,
                    hours_worked=5,
                    date=datetime.date(2020, 4, 18),
                ),
                EmployeeWorkUnit(
                    id=4,
                    report_id=1,
                    employee_id=2,
                    hours_worked=1.3,
                    date=datetime.date(2020, 4, 19),
                ),
            ],
            [
                {
                    "amountPaid": "$50.00",
                    "employeeId": "1",
                    "payPeriod": {
                        "endDate": "2021-10-15",
                        "startDate": "2021-10-01",
                    },
                },
                {
                    "amountPaid": "$189.00",
                    "employeeId": "2",
                    "payPeriod": {
                        "endDate": "2020-04-30",
                        "startDate": "2020-04-16",
                    },
                },
                {
                    "amountPaid": "$75.00",
                    "employeeId": "2",
                    "payPeriod": {
                        "endDate": "2021-10-15",
                        "startDate": "2021-10-01",
                    },
                },
            ],
        ),
    ])
    def test_generate_report(self, employees, work_reports, work_units, expected_result):
        """ Default EmployeeController::generate_report """
        with self.app.app_context():
            for employee in employees:
                self.session.add(employee)

            for work_report in work_reports:
                self.session.add(work_report)

            self.session.flush()
            for work_unit in work_units:
                self.session.add(work_unit)
            self.session.flush()

            assert self._get_controller().generate_report() == expected_result

    def test_process_csv(self):
        """ Default EmployeeController::process_csv """
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(['date', 'hours worked', 'employee id', 'job group'])
        writer.writerow(['12/10/2021', '3.5', '3', 'A'])
        writer.writerow(['19/10/2021', '2', '3', 'A'])
        writer.writerow(['12/10/2021', '1', '2', 'B'])
        output.seek(0)
        source = FileStorage(io.BytesIO(bytes(output.getvalue(), 'UTF-8')), filename='time-report-10.csv')

        with self.app.app_context():
            self._clean_db_queries()
            self._get_controller().process_csv(source)

            assert Employee.query.count() == 2
            assert Employee.query.get(3).job_group == 'A'
            assert Employee.query.get(2).job_group == 'B'

            assert EmployeeWorkReport.query.count() == 1
            assert EmployeeWorkReport.query.first().id == 10

            assert EmployeeWorkUnit.query.count() == 3
            assert EmployeeWorkUnit.query.filter_by(employee_id=3, report_id=10).count() == 2
            assert EmployeeWorkUnit.query.filter_by(employee_id=2, report_id=10).count() == 1

            hours_by_employee = {3: 5.5, 2: 1}
            for employee_id, expected_accumulated_hours in hours_by_employee.items():
                hours_for_employee_3 = sum([
                    unit.hours_worked
                    for unit
                    in EmployeeWorkUnit.query.filter_by(employee_id=employee_id, report_id=10)
                ])
                assert hours_for_employee_3 == expected_accumulated_hours
