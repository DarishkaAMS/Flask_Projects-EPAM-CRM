"""
This module consists of the:
 - Department class to work with the `departments` table
"""
from uuid import uuid4

from .. import db


class Department(db.Model):
    """
    Define the Department data model
    """

    __tablename__ = 'departments'
    # id = db.Column(db.Integer(), primary_key=True)
    # department_id = db.Column(db.Integer(), primary_key=True)
    department_id = db.Column(db.String(36), primary_key=True, index=True, default=uuid4)
    name = db.Column(db.String(25), unique=True)
    code = db.Column(db.Integer)
    employees = db.relationship('Employee', backref='departments', lazy='dynamic')
    # employees = db.relationship('Employee', backref='department', lazy='dynamic')

    def __init__(self, name, code):
        self.name = name
        self.code = code

    def to_dict(self):
        """
        Serializer that returns a dictionary from its fields
        :return: the department in json format
        """
        return {
            'department_id': self.department_id,
            'name': self.name,
            'code': self.code,
            'employees': [employee.to_dict() for employee in self.employees]
        }

    def __repr__(self):
        """
        Representation of the department
        :return: a string representing the department by name
        """
        return f"{self.name} Department"
