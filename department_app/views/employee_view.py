"""
This module represents the logic on employees routes starting with:
 - /employees/<int:page>
 - /employees/create
 - /employees/employee/<int:id>
 - /employees/assign/<int:id>
 - /employees/employee/<int:id>/update
 - /employees/employee/<int:id>/delete
"""

# pylint: disable=cyclic-import
# pylint: disable=import-error
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_required
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import url_for, request, redirect, session
# pylint: disable=relative-beyond-top-level
from .. import create_app, db
from ..models.employee import Employee, Role
from ..forms.employee import EmployeeAssignForm, EmployeeForm, EmployeeDateInfoForm, RegisterForm
from flask_user import roles_required

from . import user

app = create_app()


@user.route('/employees/<int:page>', methods=['GET', 'POST'])
@roles_required(['hr', 'head_of_department', 'employee'])
def retrieve_employees(page=1):
    """
    Handle requests to the /employees/<int:page> route - @roles_required(xxx)
    Retrieve all employee from the DB ordered by the First Name with the pagination support
    Filter employees based on specified start date and end date
    """

    employees_per_page = 7
    employees = Employee.query.order_by(Employee.first_name).paginate(page, employees_per_page, error_out=False)

    form = EmployeeDateInfoForm()
    if form.validate_on_submit():

        start_date = form.start_date.data
        end_date = form.end_date.data
        filtered_employees = Employee.query.filter(Employee.date_of_birth <= end_date).\
            filter(start_date <= Employee.date_of_birth).paginate(page, employees_per_page, error_out=False)

        if not filtered_employees.items:
            app.logger.info(f'Employee unsuccessfully filtered employees with {start_date} and {end_date}')
            flash('I can\'t find anyone within specified range. Please try again', category='danger')

        app.logger.info(f'Employee successfully filtered employees with {start_date} and {end_date}')
        return render_template('employees/employees.html', employees=filtered_employees, form=form)

    app.logger.info(f'User visited employees/employees page')
    return render_template('employees/employees.html', employees=employees, form=form)

#
# @user.route('/date', methods=['GET', 'POST'])
# def date():
#     start_date = session['start_date']
#     end_date = session['end_date']
#     return render_template('employees/date.html')


@user.route('/employees/create', methods=['GET', 'POST'])
@roles_required(['hr'])
def create_employee():
    """
    Handle requests to the /employees/create route - @roles_required(xxx)
    Add an employee to the DB using RegisterForm and required checks
    Redirect to employees page after successful employee creation
    """
    add_employee = True

    form = RegisterForm()
    if request.method == 'POST':
        first_name = form.first_name.data
        last_name = form.last_name.data
        email_address = form.email_address.data
        role = form.role.data
        date_of_birth = form.date_of_birth.data
        password_hash = form.password_hash.data
        confirm_password = form.confirm_password.data

        if len(password_hash) < 6:
            flash('Password must be at least 6 characters.', category='danger')
        elif password_hash != confirm_password:
            flash('Passwords don\'t match.', category='danger')
        elif Employee.query.filter_by(email_address=email_address).first():
            flash('I have already registered an Employee with such email', category='danger')
        elif not role:
            flash('We won\'t go any further unless you specify Employee role', category='danger')
        else:
            employee_to_create = Employee(
                first_name=first_name,
                last_name=last_name,
                email_address=email_address,
                date_of_birth=date_of_birth,
                password_hash=generate_password_hash(form.password_hash.data, method='sha256'),
            )
            employee_to_create.roles.append(Role(name=role))
            db.session.add(employee_to_create)
            db.session.commit()

            app.logger.info(f'Employee with ID {employee_to_create.id} has been created')
            flash(f'You have successfully added a new Employee - '
                  f'{employee_to_create.first_name} {employee_to_create.last_name}.', category='success')
            return redirect(url_for('user.retrieve_employees', page=1))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('auth/register.html', form=form, add_employee=add_employee)


@user.route('/employees/employee/<int:id>', methods=['GET', 'POST'])
@roles_required(['hr', 'head_of_department', 'employee'])
def retrieve_employee(id):
    """
    Handle requests to the /employees/employee/<int:id> route - @roles_required(xxx)
    Retrieve the employee with specified ID from the DB
    """
    employee = Employee.query.get_or_404(id)
    app.logger.info(f'Employee with ID {employee.id} has been retrieved')
    return render_template('employees/employee.html', employee=employee)


@user.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@roles_required(['hr'])
def assign_employee(id):
    """
    Handle requests to the /employees/assign/<int:id> route - @roles_required(xxx)
    Assign a department and salary to an employee with specified ID
    """
    employee_to_assign = Employee.query.get_or_404(id)
    form = EmployeeAssignForm(obj=employee_to_assign)

    if request.method == 'POST':
        employee_to_assign.department = form.department.data
        employee_to_assign.salary = form.salary.data
        db.session.add(employee_to_assign)
        db.session.commit()
        app.logger.info(f'Employee with ID {employee_to_assign.id} has been assigned')
        flash(f'You have successfully assigned an {employee_to_assign.first_name} {employee_to_assign.last_name}.',
              category='success')

        return redirect(url_for('user.retrieve_employees', page=1))

    app.logger.info(f'Employee with ID {employee_to_assign.id} is about to be assigned')
    return render_template('employees/assign_employee.html',
                           employee=employee_to_assign, form=form)


@user.route('/employees/employee/<int:id>/update', methods=['GET', 'POST'])
@roles_required(['hr', 'head_of_department', 'employee'])
def update_employee(id):
    """
    Handle requests to the /employees/employee/<int:id>/update route - @roles_required(xxx)
    Update an employee with specified ID
    """

    employee = Employee.query.get_or_404(id)
    form = EmployeeForm(obj=employee)

    if form.validate_on_submit():
        employee.first_name = form.first_name.data
        employee.last_name = form.last_name.data
        employee.email_address = form.email_address.data
        employee.date_of_birth = form.date_of_birth.data
        db.session.commit()
        app.logger.info(f'Employee with ID {employee.id} is updated')
        flash(f'You have successfully updated {employee.first_name} {employee.last_name} Account.',
              category='success')

        return redirect(url_for('user.retrieve_employees', page=1))

    elif request.method == 'GET':
        form.first_name.data = employee.first_name
        form.last_name.data = employee.last_name
        form.email_address.data = employee.email_address
        form.date_of_birth.data = employee.date_of_birth

    app.logger.info(f'Employee with ID {employee.id} is about to be updated')
    return render_template('employees/update_employee.html', form=form)


# pylint: disable=invalid-name
@user.route('/employees/employee/<int:id>/delete', methods=['GET', 'POST'])
@roles_required(['hr'])
def delete_employee(id):
    """
    Handle requests to the /employees/employee/<int:id>/delete route - @roles_required(xxx)
    Delete an employee with specified ID redirecting to the home page.
    """

    employee = Employee.query.get_or_404(id)
    if employee:
        db.session.delete(employee)
        db.session.commit()
        app.logger.info(f'Employee with ID {employee.id} is deleted')
        flash('You have successfully deleted the employee.', category='success')

    return redirect(url_for('user.home_page'))
