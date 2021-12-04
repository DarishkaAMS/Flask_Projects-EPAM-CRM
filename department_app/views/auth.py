"""
This module represents the logic on routes starting with /register, /login and /logout
"""
# pylint: disable=cyclic-import
# pylint: disable=import-error
import datetime
from flask import render_template, redirect, url_for, flash, request
# from flask.ext.mail import Message
from flask_login import login_user, logout_user, login_required
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash

# pylint: disable=relative-beyond-top-level
from .. import create_app, db
from ..models.employee import Employee
from ..forms.employee import RegisterForm, LoginForm
from ..token import confirm_token, generate_confirmation_token

from . import user


# app = create_app()
# mail = Mail()
# mail.init_app(app)


@user.route('/register', methods=['GET', 'POST'])
def register_page():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    form = RegisterForm()
    # if form.validate_on_submit():
    if request.method == 'POST':
        form = RegisterForm()
        first_name = form.first_name.data
        last_name = form.last_name.data
        email_address = form.email_address.data
        access_level = form.access_level.data
        date_of_birth = form.date_of_birth.data
        password_hash = form.password_hash.data
        confirm_password = form.confirm_password.data
        confirmed = False

        if len(password_hash) < 6:
            flash('Password must be at least 6 characters.', category='danger')
        elif password_hash != confirm_password:
            flash('Passwords don\'t match.', category='danger')
            # IF EMAIL IS ALREADY Exist
        elif Employee.query.filter_by(email_address=email_address).first():
            flash('I have already registered an Employee with such email', category='danger')
        else:

            if access_level == "3":
                department_id = 1
            print("department_id", access_level,department_id, type(department_id))
            employee_to_create = Employee(
                first_name=first_name,
                last_name=last_name,
                email_address=email_address,
                department_id=department_id,
                access_level=access_level,
                date_of_birth=date_of_birth,
                password_hash=generate_password_hash(form.password_hash.data, method='sha256'),
            )

            db.session.add(employee_to_create)
            db.session.commit()

            # token = generate_confirmation_token(employee_to_create.email_address)
            # confirm_url = url_for('user.confirm_email', token=token, _external=True) # To check user.confirm_email
            # html = render_template('auth/activate.html', confirm_url=confirm_url)
            # subject = "Please confirm your email"
            # send_email(employee_to_create.email_address, subject, html)

            # msg = Message(
            #     subject,
            #     sender="honeydummyams@gmail.com",
            #     recipients=['honeydummyams@gmail.com'],
            # )
            # mail.send(msg)

            login_user(employee_to_create)
            flash(f'Account has been created successfully! You are now logged in '
                  f'as {employee_to_create.first_name} {employee_to_create.last_name}', category='success')

            return redirect(url_for('user.home_page'))

            if form.errors != {}:
                for err_msg in form.errors.values():
                    flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('auth/register.html', form=form)


@user.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email_address = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    confirmed_employee = Employee.query.filter_by(email_address=email_address).first_or_404()
    if confirmed_employee.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        confirmed_employee.confirmed = True
        confirmed_employee.confirmed_on = datetime.datetime.now()
        db.session.add(confirmed_employee)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('home'))


# def send_email(to, subject, template):
#     msg = Message(
#         subject,
#         recipients=[to],
#         html=template,
#         sender=app.config['MAIL_DEFAULT_SENDER']
#     )
#     mail.send(msg)


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

        attempted_employee = Employee.query.filter_by(email_address=email_address).first()
        if attempted_employee:
            if check_password_hash(attempted_employee.password_hash, password_hash):
                login_user(attempted_employee)
                flash(f'Success! You are logged in as '
                      f'{attempted_employee.first_name} {attempted_employee.last_name}', category='success')
                return redirect(url_for('user.home_page'))
            else:
                flash('Incorrect password, please, try again.', category='danger')

        elif not attempted_employee:
            flash('This Employee does not exist!', category='danger')

        else:
            flash('Email and password are not match! Please try again!', category='danger')

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

    return redirect(url_for('user.home_page'))
