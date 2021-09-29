"""
Employee-related models.
"""
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Date

from app.database import DATABASE


class Employee(DATABASE.Model):
    """
    Employee base model.
    """
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    job_group = Column(String(1))


class EmployeeWorkUnit(DATABASE.Model):
    """
    Represents a unit of data for a work entry for a certain employee.
    """
    __tablename__ = 'employee_work_units'

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey(Employee.id), nullable=False)
    time_report_id = Column(Integer, nullable=False)
    hours_worked = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
