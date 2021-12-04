"""
This module consists of the class Employee to work with `employees` table
"""
from datetime import date
from flask_login import UserMixin

from .. import bcrypt, db, login_manager
from .department import Department

ACCESS = {
    'guest': 0,
    'employee': 1,
    'head_of_dep': 2,
    'hr': 3
}


class Employee (db.Model, UserMixin):
    """
    Create an Employee instance
    """

    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    email_address = db.Column(db.String(50), nullable=False, unique=True)
    access_level = db.Column(db.Integer)
    # confirmed = False
    date_of_birth = db.Column(db.Date)
    salary = db.Column(db.Integer, default=1)
    password_hash = db.Column(db.String(length=150), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    def __init__(self, first_name, last_name, email_address, access_level, date_of_birth, password_hash,
                 salary=None, confirmed=False, department_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.access_level = access_level
        self.confirmed = confirmed
        self.date_of_birth = date_of_birth
        self.salary = salary
        self.password_hash = password_hash
        self.department_id = department_id

    def is_admin(self):
        return self.access == ACCESS['hr']

    def allowed(self, access_level):
        return self.access >= access_level

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
        # return f"Employee - {self.id}"
        return f"{self.first_name} {self.last_name}"


@login_manager.user_loader
def load_user(user_id):
    """
    Load User
    :param user_id:
    :return:
    """
    return Employee.query.get(int(user_id))
