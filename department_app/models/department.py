"""
This module consists of the class Department to work with `departments` table
"""

from .. import db


class Department(db.Model):
    """
    Create a Department instance
    """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True)
    head = db.Column(db.String(25))
    employee = db.relationship('Employee', backref='department', lazy='dynamic')

    def to_dict(self):
        """
        Serializer that returns a dictionary from its fields
        :return: the department in json format
        """
        return {
            'id': self.id,
            'name': self.name,
            'head': self.head,
            'employees': [employee.to_dict() for employee in self.employees]
        }

    def __repr__(self):
        """
        Representation of the department
        :return: a string representing the department by name
        """
        return f"<{self.name} Department>"
