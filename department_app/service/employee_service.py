"""
This module consists of the CRUD operations to work with `employees` table
"""

from datetime import datetime

from .. import db

from ..models.employee import Employee


def get_all_employees():
    """
    Get all records from the employees table
    :return: the list of all employees
    """
    # in json format?
    employees = Employee.query.all()
    return [employee.to_dict() for employee in employees]


def add_employee(first_name, last_name, email_address, department_id, date_of_birth, salary, password):
    """
    Add a new Employee to the employees table
    :param first_name: the Employee's first name
    :param last_name: the Employee's last name
    :param email_address: the Employee's email address
    :param department_id: the Department's id
    :param date_of_birth: the Employee's date of birth
    :param salary: the Employee's salary
    :param password: the employee password

    """
    date_of_birth = datetime.strptime(date_of_birth, '%m/%d/%Y')
    employee = Employee(
        first_name=first_name,
        last_name=last_name,
        email_address=email_address,
        # department_id=department_id,
        date_of_birth=date_of_birth,
        # salary=salary,
        password=password,
    )

    db.session.add(employee)
    db.session.commit()


def update_employee(id, first_name, last_name, email_address, department_id, date_of_birth, salary):
    """
    Update an existing Employee
    :param id: id of required Employee to be updated
    :param first_name: the Employee's first name
    :param last_name: the Employee's last name
    :param email_address: the Employee's email address
    :param department_id: the Department's id
    :param date_of_birth: the Employee's date of birth
    :param salary: the Employee's salary
    """
    employee = Employee.query.get_or_404(id)

    employee.first_name = first_name
    employee.last_name = last_name
    employee.email_address = email_address
    employee.department_id = department_id
    employee.date_of_birth = date_of_birth
    employee.salary = salary

    db.session.add(employee)
    db.session.commit()


def update_employee_patch(id, first_name, last_name, email_address, department_id, date_of_birth, salary):
    """
    Update an existing employee without overwriting the unspecified elements with null
    :param id: id of required Employee to be updated
    :param first_name: the Employee's first name
    :param last_name: the Employee's last name
    :param email_address: the Employee's email address
    :param department_id: the Department's id
    :param date_of_birth: the Employee's date of birth
    :param salary: the Employee's salary
    """
    employee = Employee.query.get_or_404(id)

    if first_name:
        employee.first_name = first_name
    elif last_name:
        employee.last_name = last_name
    elif email_address:
        employee.email = email_address
    elif department_id:
        employee.department_id = department_id
    elif date_of_birth:
        employee.date_of_birth = date_of_birth
    elif salary:
        employee.salary = salary

    db.session.add(employee)
    db.session.commit()


def delete_employee(id):
    """
    Delete an existing Employee
    :param id: id of required Employee to be deleted
    """
    employee = Employee.query.get_or_404(id)

    db.session.delete(employee)
    db.session.commit()


def get_employee_by_id(id):
    """
    Get the Employee by id
    :param id: id of required Employee
    :return: the Employee by the specified id
    """
    employee = Employee.query.get(id)
    return employee.to_dict()


def get_all_employees_in_department(department):
    """
    Get all employees in specified Department
    :return: the list of employees from the specified Department
    """
    employees = Employee.query.filter_by(department_id=department['id']).all()
    return [employee.to_dict() for employee in employees]


def get_employees_born_on(date):
    """
    Get all employees born on a specified date
    :param date: the date to filter with
    :return: the list of employees born on a specified date
    """
    date = datetime.strptime(date, '\'%m/%d/%Y\'').date()
    employees = Employee.query.filter_by(date_of_birth=date)
    return [employee.to_dict() for employee in employees]


def get_employees_born_between(start_date, end_date):
    """
    Get all employees born between specified end and start dates
    :param start_date: the date to start comparison with
    :param end_date: the date to end comparison with
    :return: the list of employees born between start and end dates
    """
    start_date = datetime.strptime(start_date, '\'%m/%d/%Y\'').date()
    end_date = datetime.strptime(end_date, '\'%m/%d/%Y\'').date()
    # get all employees
    employees = Employee.query.all()
    # filter employees by birthday
    return [employee.to_dict() for employee in employees
            if start_date <= employee.date_of_birth <= end_date]
