from flask import Blueprint, flash, render_template, request

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@auth.route('/logout')
def logout():
    return '<h2> LOGOUT </h2>'


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(first_name) < 2:
            flash('First name must be greater than 2 characters.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 2 characters.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        else:
            flash('Account has been creates', category='success')

    return render_template('sign_up.html')


