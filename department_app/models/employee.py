"""
This module consists of the:
 - Employee class to work with the `employees` table
 - Role class to work with the `roles` table
 - UserRoles class to work with the `employees_roles` table
 - load_user function to return Employee by the specified employee_id
"""

from flask_login import UserMixin
from uuid import uuid4

from .. import db, login_manager
from .department import Department

ACCESS = {
    'guest': 0,
    'employee': 1,
    'head_of_dep': 2,
    'hr': 3
}


class Employee(db.Model, UserMixin):
    """
    Define the Employee data model
    """
    __tablename__ = 'employees'
    employee_id = db.Column(db.Integer(), primary_key=True)
    # employee_id = db.Column(db.String(36), primary_key=True, index=True, default=uuid4)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    email_address = db.Column(db.String(50), nullable=False, unique=True)
    date_of_birth = db.Column(db.Date)
    salary = db.Column(db.Integer, default=1)
    password_hash = db.Column(db.String(length=150), nullable=False)
    department_id = db.Column(db.String(36), db.ForeignKey('departments.department_id'))
    roles = db.relationship('Role', secondary='employees_roles',
                            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, first_name, last_name, email_address, date_of_birth, password_hash,
                 salary=1, department_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
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
            'employee_id': self.employee_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email_address': self.email_address,
            'department': Department.query.get_or_404(self.department_id).name,
            'date_of_birth': self.date_of_birth.strftime('%m/%d/%Y'),
            'salary': self.salary,
        }

    def has_roles(self, *args):
        for role in self.roles:
            return role.name in set(*args)
        # return set(args).issubset({role.name for role in self.roles})

    def __repr__(self):
        """
        Representation of the Employee
        :return: a string representing the employee by first name and last name
        """
        # return f"Employee - {self.employee_id}"
        return f"{self.first_name} {self.last_name}"


class Role(db.Model):
    """
    Define the Role data model
    """
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    # id = db.Column(db.String(36), primary_key=True, index=True, default=uuid4)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return (self.name == other or
                self.name == getattr(other, 'name', None))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        """
        Representation of the Role
        :return: a string representing the role by its name
        """
        return f'<Role: {self.name}>'


class UserRoles(db.Model):
    """
    Define the UserRoles data model
    """
    __tablename__ = 'employees_roles'

    id = db.Column(db.Integer(), primary_key=True)
    # id = db.Column(db.String(36), primary_key=True, index=True, default=uuid4)
    user_id = db.Column(db.Integer(), db.ForeignKey('employees.employee_id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

    def __repr__(self):
        """
        Representation of the UserRoles
        :return: a string representing the user role by User/Employee ID
        """
        return f'<Role: {self.role_id}>'


@login_manager.user_loader
def load_user(employee_id):
    """
    Load User
    :param employee_id:
    :return Employee by the specified employee_id:
    """
    # Do not convert into the INT!!!
    return Employee.query.get(employee_id)
    # return Employee.query.get(int(employee_id))
