"""
Employee-related models.
"""
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from app.database import DATABASE


class Employee(DATABASE.Model):
    """
    Employee base model.
    """
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    job_group = Column(String(1))


class EmployeeWorkReport(DATABASE.Model):
    """
    Represents the report generated from the CSV file.
    """
    __tablename__ = 'employee_work_reports'

    id = Column(Integer, primary_key=True)


class EmployeeWorkUnit(DATABASE.Model):
    """
    Represents a unit of data for a work entry for a certain employee.
    """
    __tablename__ = 'employee_work_units'

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey(Employee.id), nullable=False)
    report_id = Column(Integer, ForeignKey(EmployeeWorkReport.id), nullable=False)
    hours_worked = Column(Float, nullable=False)
    date = Column(Date, nullable=False)

    employee = relationship(Employee, uselist=False)
