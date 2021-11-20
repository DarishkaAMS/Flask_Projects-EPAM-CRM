from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html', text="TESTING")


@auth.route('/logout')
def logout():
    return '<h2> LOGOUT </h2>'


@auth.route('/sign-up')
def sign_up():
    return render_template('sign_up.html')


@auth.route('/new')
def new():
    return render_template('create_employee.html')
