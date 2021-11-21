from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_user, logout_user
# from ..models.employee import Employee

from . import app, db
from .forms import LoginForm, RegisterForm
from .models import Employee, Department

# routes = Blueprint('routes', __name__)


@app.route('/')
@app.route('/home')
def home_page_view():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page_view():
    form = RegisterForm()

    if form.validate_on_submit():
        new_employee = Employee(first_name=form.first_name.data, last_name=form.last_name.data,
                                email_address=form.email_address.data, date_of_birth=form.date_of_birth.data,
                                department=form.department.data, salary=form.salary.data, password=form.password_1.data)
        db.session.add(new_employee)
        db.session.commit()
        login_user(new_employee)
        flash(f"Account created successfully! You are logged in as {new_employee.first_name} {new_employee.last_name}",
              category='success')
        return redirect(url_for('home_page_view'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating an Employee\'s account: {err_msg}', category='danger')

    print("DEP is created")
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page_view():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_employee = Employee.query.filter_by(email_address=form.email_address.data).first()
        if attempted_employee and attempted_employee.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_employee)
            flash(f'Welcome Back, {attempted_employee.first_name} {attempted_employee.last_name}!', category='success')
            # UPDATE TO DEPARTMENT
            return redirect(url_for('home_page_view'))
        else:
            flash('Sorry... But email and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page_view():
    logout_user()
    flash('Bye now! Come back again!', category='info')
    return redirect(url_for('home_page_view'))


@app.route('/departments')
def departments_page_view():
    departments = Department.query.all()
    return render_template('departments.html', departments=departments)



#
# @app.route('/employee')
# def employee_view_page:
