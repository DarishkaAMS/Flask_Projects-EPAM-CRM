"""
This module represents the logic on routes starting with /employees
"""

# pylint: disable=cyclic-import
# pylint: disable=import-error
from flask import render_template, redirect, url_for, flash
from flask_login import login_required

# pylint: disable=relative-beyond-top-level
from .. import db
from ..models.employee import Employee
from ..forms.employee import EmployeeAssignForm, EmployeeForm

from . import user


@user.route('/employees')
@login_required
def show_employees():
    """
    Show all employees
    """
    employees = Employee.query.all()

    return render_template('employees/employees.html', employees=employees)


# pylint: disable=invalid-name
# pylint: disable=redefined-builtin
@user.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    """
    Assign a department to an employee
    """
    employee_to_assign = Employee.query.get_or_404(id)

    form = EmployeeAssignForm(obj=employee_to_assign)
    if form.validate_on_submit():
        employee_to_assign.department = form.department.data
        # pylint: disable=no-member
        db.session.add(employee_to_assign)
        db.session.commit()
        flash('You have successfully assigned a department.', category='success')

        # redirect to the employees page
        return redirect(url_for('user.show_employees'))

    return render_template('employees/assign_employee.html',
                           employee=employee_to_assign, form=form)


@user.route('/employees/add', methods=['GET', 'POST'])
@login_required
def add_employee():
    """
    Add an employee to the database
    """
    add_emp = True

    form = EmployeeForm()
    if form.validate_on_submit():
        employee_to_add = Employee(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email_address=form.email_address.data,
            date_of_birth=form.date_of_birth.data,
            department=form.department.data,
            salary=form.salary.data,
        )
        try:
            # pylint: disable=no-member
            # add employee to the database
            db.session.add(employee_to_add)
            db.session.commit()
            flash('You have successfully added a new employee.', category='success')
        # pylint: disable=bare-except
        except:
            flash('Something went wrong when creating a new employee.', category='danger')

        # redirect to employee page
        return redirect(url_for('user.show_employees'))

    # load employee template
    return render_template('employees/employee.html', action='Add',
                           add_emp=add_emp, form=form)


# pylint: disable=invalid-name
@user.route('/employees/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_employee(id):
    """
    Edit an employee
    """
    add_emp = False

    employee = Employee.query.get_or_404(id)
    form = EmployeeForm(obj=employee)
    if form.validate_on_submit():
        first_name = form.first_name.data,
        last_name = form.last_name.data,
        email_address = form.email_address.data,
        date_of_birth = form.date_of_birth.data,
        department = form.department.data,
        salary = form.salary.data,
        # pylint: disable=no-member
        db.session.commit()
        flash('You have successfully edited the employee.', category='success')

        # redirect to the employees page
        return redirect(url_for('user.show_employees'))

    form.first_name.data = employee.first_name,
    form.last_name.data = employee.last_name,
    form.email_address.data = employee.email_address,
    form.date_of_birth.data = employee.date_of_birth,
    form.department.data = employee.department,
    form.salary.data = employee.salary,
    return render_template('employees/employee.html', action="Edit",
                           add_emp=add_emp, form=form,
                           employee=employee)


# pylint: disable=invalid-name
@user.route('/employees/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_employee(id):
    """
    Delete an employee from the database
    """
    employee = Employee.query.get_or_404(id)
    # pylint: disable=no-member
    db.session.delete(employee)
    db.session.commit()
    flash('You have successfully deleted the employee.', category='success')

    # redirect to the employees page
    return redirect(url_for('user.show_employees'))