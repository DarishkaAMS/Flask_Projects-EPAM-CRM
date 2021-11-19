from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return '<h2> LOGIN </h2>'


@auth.route('/logout')
def logout():
    return '<h2> LOGOUT </h2>'


@auth.route('/sign-up')
def sign_up():
    return '<h2> SIGN UP </h2>'


@auth.route('/new')
def new():
    return render_template('create_employee.html')
