"""
This module represents the logic on routes starting with /employees
"""

# pylint: disable=cyclic-import
# pylint: disable=import-error
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_required

# pylint: disable=relative-beyond-top-level
from .. import db
from ..models.employee import Employee
from ..forms.employee import EmployeeAssignForm, EmployeeForm, RegisterForm, EmployeeDateInfoForm

from . import user


@user.route('/employees/<int:page>', methods=['GET', 'POST'])
@login_required
def retrieve_employees(page=1):
    """
    Show all employees
    """
    # employees = Employee.query.order_by(Employee.first_name).all()
    employees_per_page = 10
    employees = Employee.query.order_by(Employee.first_name).paginate(page, employees_per_page, error_out=False)
    pagination_tag = True

    form = EmployeeDateInfoForm()
    if form.validate_on_submit():
        # session['start_date'] = form.start_date.data
        # session['end_date'] = form.end_date.data
        employee_list = []
        # from datetime import date
        # start = date(year=1900, month=11, day=1)
        # end = date(year=2021, month=11, day=1)

        start_date = form.start_date.data
        end_date = form.end_date.data

        print("start_date", start_date)
        # filtered_employees = Employee.query.filter(start_date <= Employee.date_of_birth)
        filtered_employees = Employee.query.filter(Employee.date_of_birth <= end_date).filter(start_date <= Employee.date_of_birth)
        for employee in filtered_employees:
            print(employee.date_of_birth)


        # for employee in employees.items:
        #     if employee.date_of_birth:
        #         if session['start_date'] < employee.date_of_birth < session['end_date']:
        #             employee_list.append(employee)


        # IF date range is wrong
        pagination_tag = False
        return render_template('employees/employees.html', employees=filtered_employees, form=form, pagination_tag=pagination_tag)

    return render_template('employees/employees.html', employees=employees, form=form, pagination_tag=pagination_tag)


@user.route('/date', methods=['GET', 'POST'])
def date():
    start_date = session['start_date']
    end_date = session['end_date']
    return render_template('employees/date.html')


@user.route('/employees/create', methods=['GET', 'POST'])
@login_required
def create_employee():
    """
    Add an employee to the database
    """
    add_employee = True

    form = RegisterForm()
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
        return redirect(url_for('user.retrieve_employees'))

    # load employee template
    return render_template('auth/register.html', form=form, add_employee=add_employee)


@user.route('/employees/employee/<int:id>', methods=['GET', 'POST'])
@login_required
def retrieve_employee(id):
    """
    Show employee
    """
    employee = Employee.query.get_or_404(id)

    return render_template('employees/employee.html', employee=employee)


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
        employee_to_assign.salary = form.salary.data
        # print("employee_to_assign.salary", employee_to_assign.salary)
        db.session.add(employee_to_assign)
        db.session.commit()
        flash('You have successfully assigned an Employee.', category='success')

        # redirect to the employees page
        return redirect(url_for('user.retrieve_employee', id=employee_to_assign.id))

    return render_template('employees/assign_employee.html',
                           employee=employee_to_assign, form=form)


# pylint: disable=invalid-name
@user.route('/employees/employee/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_employee(id):
    """
    Edit an employee
    """
    add_emp = False
    # if post.author != current_user:
    #     abort(403)
    employee = Employee.query.get_or_404(id)
    form = EmployeeForm(obj=employee)

    if form.validate_on_submit():
        employee.first_name = form.first_name.data
        employee.last_name = form.last_name.data
        employee.email_address = form.email_address.data
        employee.date_of_birth = form.date_of_birth.data

        db.session.commit()
        flash('You have successfully edited Your Account.', category='success')

        return redirect(url_for('user.retrieve_employee', id=employee.id))

    elif request.method == 'GET':
        form.first_name.data = employee.first_name
        form.last_name.data = employee.last_name
        form.email_address.data = employee.email_address
        form.date_of_birth.data = employee.date_of_birth

    return render_template('employees/update_employee.html', title='Update Employee',
                           form=form, legend='Update Employee')


# pylint: disable=invalid-name
@user.route('/employees/employee/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_employee(id):
    """
    Delete an employee from the database
    """
    # I DELETE MYSELF!!!!
    employee = Employee.query.get_or_404(id)
    # pylint: disable=no-member
    db.session.delete(employee)
    db.session.commit()
    flash('You have successfully deleted the employee.', category='success')

    # redirect to the employees page
    return redirect(url_for('user.home_page'))


def pagination(page):
    page = page
    pages = 5
    #employees = Employees.query.filter().all()
    #employees = Employees.query.paginate(page,pages,error_out=False)
    employees = Employee.query.order_by(Employee.first_name).paginate(page, pages, error_out=False)
