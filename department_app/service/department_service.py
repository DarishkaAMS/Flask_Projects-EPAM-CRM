"""
This module consists of the CRUD operations to work with `departments` table
"""

from .. import db
from ..models.department import Department
from ..models.employee import Employee


def get_all_departments():
    """
    Select all existing Departments
    :return: the list of all departments
    """
    # in json format?
    departments = Department.query.all()
    return [department.to_dict() for department in departments]


def add_department(name, code):
    """
    Add a new Department to the departments table
    :param name: the Department's name
    :param code: the Department's code
    """
    department = Department(name=name, code=code)

    db.session.add(department)
    db.session.commit()


def update_department(id, name, code):
    """
    Update an existing Department by id
    :param id: id of updating Department
    :param name: the Department's name
    :param code: the Department's code
    """
    department = Department.query.get_or_404(id)
    department.name = name
    department.code = code

    db.session.add(department)
    db.session.commit()


def update_department_patch(id, name, code):
    """
    Update an existing department without overwriting the unspecified elements with null
    :param id: id of updating Department
    :param name: the Department's name
    :param code: the Department's code
    """
    department = Department.query.get_or_404(id)
    if name:
        department.name = name
    elif code:
        department.description = code

    db.session.add(department)
    db.session.commit()


def delete_department(id):
    """
    Delete a Department by id
    :param id: id of deleting Department
    """
    department = Department.query.get_or_404(id)

    db.session.delete(department)
    db.session.commit()


def get_department_by_id(id):
    """
    Get a specific Department from departments table by id
    :param id: id of the required Department
    :return: the Department with a specified id
    """
    department = Department.query.get(id)
    return department.to_dict()


def get_average_salary(department):
    """
    Get an average salary of all employees in the specified Department
    :return: the average salary of all employees in the specified Department
    """
    employees = Employee.query.filter_by(department_id=department['id']).all()
    average_salary = 0

    for employee in employees:
        average_salary += employee.salary

    # What if there are no employees?
    if len(employees) > 0:
        average_salary /= len(employees)

    return round(average_salary, 2)


# Do we really need this?
def get_average_age(department):
    """
    Get an average age of all employees in the specified Department
    :return: the average age of all employees in the specified Department
    """
    employees = Employee.query.filter_by(department_id=department['id']).all()
    average_age = 0

    for employee in employees:
        average_age += employee.calculate_age(employee.birthday)

    if len(employees) > 0:
        average_age /= len(employees)

    return round(average_age, 1)
