from flask import Blueprint

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
