"""
This module represents the logic on routes starting with /register, /login and /logout
"""
# pylint: disable=cyclic-import
# pylint: disable=import-error
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

# pylint: disable=relative-beyond-top-level
from .. import db
from ..models.employee import Employee
from ..forms.employee import RegisterForm, LoginForm

from . import user


@user.route('/register', methods=['GET', 'POST'])
def register_page():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    form = RegisterForm()
    if form.validate_on_submit():
        employee_to_create = Employee(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email_address=form.email_address.data,
            # date_of_birth=form.date_of_birth.data,
            # salary=form.salary.data,
            # password_hash=form.password.data
            password_hash=generate_password_hash(form.password.data, method='sha256')

        )

        # pylint: disable=no-member
        # add employee to the database
        db.session.add(employee_to_create)
        db.session.commit()
        login_user(employee_to_create)
        flash(f'Account has been created successfully! You are now logged in '
              f'as {employee_to_create.first_name} {employee_to_create.last_name}', category='success')

        # redirect to the home page
        print("DATA, ", employee_to_create)
        return redirect(url_for('user.home_page'))

    # pylint: disable=no-member
    # if there are no errors from the validations
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    # load registration template
    return render_template('auth/register.html', form=form)


@user.route('/login', methods=['GET', 'POST'])
def login_page():
    """
    Handle requests to the /login route
    Add an employee to the database through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # pylint: disable=no-else-return
        attempted_employee = Employee.query.filter_by(email_address=form.email_address.data).first()
        if attempted_employee and attempted_employee.check_password_correction(
                attempted_password=form.password.data
        ):
            # log employee in
            login_user(attempted_employee)
            flash(f'Success! You are logged in as: '
                  f'{attempted_employee.username}', category='success')

            # redirect to the home page after login
            return redirect(url_for('user.home_page'))

        elif not attempted_employee:
            flash('This login does not exist!', category='danger')

        else:
            flash('Email and password are not match! Please try again!', category='danger')

    # load login template
    return render_template('auth/login.html', form=form)


@user.route('/logout')
@login_required
def logout_page():
    """
    Handle requests to the /logout route
    Allow employee to logout moving to home page.
    """
    logout_user()
    flash('You have been logged out See Ya!', category='info')

    # redirect to the home page
    return redirect(url_for('user.home_page'))
