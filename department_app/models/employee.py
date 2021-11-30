"""
This module consists of the class Employee to work with `employees` table
"""
from datetime import date
from flask_login import UserMixin

from .. import bcrypt, db, login_manager
from .department import Department


class Employee (db.Model, UserMixin):
    """
    Create an Employee instance
    """

    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    email_address = db.Column(db.String(50), nullable=False, unique=True)
    confirmed = False
    date_of_birth = db.Column(db.Date)
    salary = db.Column(db.Integer)
    password_hash = db.Column(db.String(length=150), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    def to_dict(self):
        """
        Serialize dictionary from its fields
        :return: the employee in json format
        """
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email_address': self.email_address,
            'department': Department.query.get_or_404(self.department_id).name,
            'date_of_birth': self.date_of_birth.strftime('%m/%d/%Y'),
            'salary': self.salary,
        }

    def __repr__(self):
        """
        Representation of the Employee
        :return: a string representing the employee by first name and last name
        """
        return f"Employee - {self.id}"


@login_manager.user_loader
def load_user(user_id):
    """
    Load User
    :param user_id:
    :return:
    """
    return Employee.query.get(int(user_id))
