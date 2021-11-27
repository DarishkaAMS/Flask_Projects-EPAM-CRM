"""
This module represents the logic on routes starting with /register, /login and /logout
"""
# pylint: disable=cyclic-import
# pylint: disable=import-error
from flask import render_template, redirect, url_for, flash, request
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

    if request.method == 'POST':
        form = RegisterForm()
        first_name = form.first_name.data
        last_name = form.last_name.data
        email_address = form.email_address.data
        password_hash = form.password_hash.data
        confirm_password = form.confirm_password.data

        if len(password_hash) < 6:
            flash('Password must be at least 6 characters.', category='error')
        elif password_hash != confirm_password:
            flash('Passwords don\'t match.', category='error')
        else:
                employee_to_create = Employee(
                    first_name=first_name,
                    last_name=last_name,
                    email_address=email_address,
                    password_hash=generate_password_hash(form.password_hash.data, method='sha256')

                )

                db.session.add(employee_to_create)
                db.session.commit()
                login_user(employee_to_create)
                flash(f'Account has been created successfully! You are now logged in '
                      f'as {employee_to_create.first_name} {employee_to_create.last_name}', category='success')

                print("DATA, ", employee_to_create)
                return redirect(url_for('user.home_page'))

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
        email_address = request.form.get('email_address')
        password_hash = request.form.get('password_hash')

        print("PASSWORD", password_hash)
        attempted_employee = Employee.query.filter_by(email_address=email_address).first()
        # if attempted_employee and attempted_employee.check_password_correction(
        #         attempted_password=form.password.data
        # ):
        if attempted_employee:
            if check_password_hash(attempted_employee.password_hash, password_hash):
                login_user(attempted_employee)
                flash(f'Success! You are logged in as '
                      f'{attempted_employee.first_name} {attempted_employee.last_name}', category='success')
                return redirect(url_for('user.home_page'))
            else:
                flash('Incorrect password, please, try again.', category='error')

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
    flash('You have been logged out. See Ya!', category='info')

    # redirect to the home page
    return redirect(url_for('user.home_page'))
