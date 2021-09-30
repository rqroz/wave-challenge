"""
Employee-related controller module.
"""
import calendar
import csv
import datetime

import io

from flask import g
from typing import List, Dict
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.constants.employees import JOB_GROUP_WAGES
from app.models.employees import Employee, EmployeeWorkReport, EmployeeWorkUnit


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

    def _recorver_report_id(self, source: FileStorage) -> int:
        default_error_msg = 'Invalid filename. Please inform a file named "time-report-{id}.csv"'

        filename = secure_filename(source.filename)
        try:
            filename_parts = filename.split('.')[0].split('-')
            report_id = int(filename_parts[2])
        except Exception:
            raise EmployeeControllerException(default_error_msg)

        if not (len(filename_parts) == 3 and filename_parts[0] == 'time' and filename_parts[1] == 'report'):
            raise EmployeeControllerException(default_error_msg)

        return report_id

    def process_csv(self, source: FileStorage):
        report_id = self._recorver_report_id(source)
        if EmployeeWorkReport.query.filter_by(id=report_id).count() != 0:
            raise EmployeeControllerException('Source file already processed')

        source_string_io = io.StringIO(source.stream.read().decode('UTF-8'), newline=None)
        csv_reader = csv.reader(source_string_io)
        next(csv_reader)  # Get rid of the header row

        report = EmployeeWorkReport(id=report_id)
        self.db_session.add(report)
        self.db_session.flush()

        employee_ids = []
        for row in csv_reader:
            date_str = row[0]
            hours_worked = float(row[1])
            employee_id = int(row[2])
            job_group = row[3]

            if employee_id not in employee_ids:
                employee = Employee.query.filter_by(id=employee_id).first()
                if not employee:
                    employee = Employee(id=employee_id, job_group=job_group)
                    self.db_session.add(employee)
                    self.db_session.flush()
                employee_ids.append(employee.id)

            work_unit_data = EmployeeWorkUnit(
                employee_id=employee_id,
                report_id=report.id,
                hours_worked=hours_worked,
                date=datetime.date(*[int(part) for part in reversed(date_str.split('/'))]),
            )
            self.db_session.add(work_unit_data)
            self.db_session.flush()

        self.db_session.commit()


    def _get_period(self, date: datetime.date) -> Dict[str, str]:
        if date.day < 15:
            first_day = 1
            final_day = 15
        else:
            first_day = 16
            final_day = calendar.monthrange(date.year, date.month)[1]

        return {
            'startDate': date.replace(day=first_day).isoformat(),
            'endDate': date.replace(day=final_day).isoformat(),
        }

    def generate_report(self) -> List[Dict[str, str]]:
        ordering = [EmployeeWorkUnit.employee_id.asc(), EmployeeWorkUnit.date.asc()]
        work_units = EmployeeWorkUnit.query.order_by(*ordering).all()

        data = {}
        for work_unit in work_units:
            employee_id = work_unit.employee_id
            if not data.get(employee_id):
                data[employee_id] = {}

            period = self._get_period(work_unit.date)
            period_slug = f'{period["startDate"]}_{period["endDate"]}'
            if not data[employee_id].get(period_slug):
                data[employee_id][period_slug] = {'amount': 0, 'payPeriod': period, 'employeeId': str(employee_id)}
            data[employee_id][period_slug]['amount'] += JOB_GROUP_WAGES[work_unit.employee.job_group] * work_unit.hours_worked

        result = []
        for employee_item in data.values():
            items = list(employee_item.values())
            for item in items:
                amount_str = '{:.2f}'.format(item.pop('amount'))
                item['amountPaid'] = f'${amount_str}'
            result += items
        return result
