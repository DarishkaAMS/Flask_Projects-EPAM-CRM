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
        date_of_birth = request.form.get('date_of_birth')
        department = request.form.get('department')
        salary = request.form.get('salary')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) == 0 or len(department) == 0 or \
                len(password1) == 0 or len(password2) == 0 or len(date_of_birth) == 0:
            flash('Fields marked with * should be filled', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 2 characters.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 2 characters.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(password1) < 3:
            flash('Password must be at least 8 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        else:
            flash('Account has been creates', category='success')
        print("DEP", first_name, last_name, date_of_birth, email, department, salary, password1, password2)
    return render_template('sign_up.html')


