# from flask import flash, redirect, render_template, request, url_for
# from flask_login import current_user, login_user, logout_user
# # from ..models.employee import Employee
#
# from . import app, db
# from .forms import LoginForm, RegisterForm, UpdateAccountForm
# from .models.department import Department
# from .models.employee import Employee
#
#
# # routes = Blueprint('routes', __name__)
#
#
# @app.route('/')
# @app.route('/home')
# def home_page_view():
#     return render_template('home.html')
#
#
# @app.route('/register', methods=['GET', 'POST'])
# def register_page_view():
#     form = RegisterForm()
#
#     if form.validate_on_submit():
#         new_employee = Employee(first_name=form.first_name.data, last_name=form.last_name.data,
#                                 email_address=form.email_address.data, date_of_birth=form.date_of_birth.data,
#                                 department=form.department.data, salary=form.salary.data, password=form.password_1.data)
#         db.session.add(new_employee)
#         db.session.commit()
#         login_user(new_employee)
#         flash(f"Employee account is created successfully! You are logged in as {new_employee.first_name} {new_employee.last_name}",
#               category='success')
#         return redirect(url_for('home_page_view'))
#
#     if form.errors != {}:
#         for err_msg in form.errors.values():
#             flash(f'There was an error with creating an Employee\'s account: {err_msg}', category='danger')
#
#     print("DEP is created")
#     return render_template('register.html', form=form)
#
#
# @app.route('/login', methods=['GET', 'POST'])
# def login_page_view():
#     if current_user.is_authenticated:
#         return redirect(url_for('home_page_view'))
#
#     form = LoginForm()
#     if form.validate_on_submit():
#         attempted_employee = Employee.query.filter_by(email_address=form.email_address.data).first()
#         if attempted_employee and attempted_employee.check_password_correction(
#                 attempted_password=form.password.data
#         ):
#             login_user(attempted_employee)
#             flash(f'Welcome Back, {attempted_employee.first_name} {attempted_employee.last_name}!', category='success')
#             # UPDATE TO DEPARTMENT
#             return redirect(url_for('departments_page_view'))
#         else:
#             flash('Sorry... But email and password are not match! Please try again', category='danger')
#
#     return render_template('login.html', form=form)
#
#
# @app.route('/logout')
# def logout_page_view():
#     logout_user()
#     flash('Bye now! Come back again!', category='info')
#     return redirect(url_for('home_page_view'))
#
#
# @app.route('/departments')
# def departments_page_view():
#     departments = Department.query.all()
#     return render_template('departments.html', departments=departments)
#
#
# @app.route('/employee/<int:id>', methods=['GET'])
# def employee_page_view(id):
#     employee = Employee.query.get_or_404(id)
#     return render_template('employee.html', employee=employee)
#
#
# @app.route('/employee/<int:id>/update', methods=['GET', 'POST'])
# def employee_update_view(id):
#     employee = Employee.query.get_or_404(id)
#     print("EMPL", employee.first_name)
#     # if employee.id != current_user:
#     #     abort(403)
#     form = UpdateAccountForm()
#     if form.validate_on_submit():
#         employee.first_name = form.first_name.data
#         employee.last_name = form.last_name.data
#         employee.email_address = form.email_address.data
#         employee.date_of_birth = form.date_of_birth.data
#         # password = form.password_1.data
#         db.session.commit()
#         flash('Everything is updated!', category='success')
#         return redirect(url_for('employee.html', id=employee.id))
#
#     elif request.method == 'GET':
#         form.first_name.data = employee.first_name
#         form.last_name.data = employee.last_name
#         form.email_address.data = employee.email_address
#         form.date_of_birth.data = employee.date_of_birth
#
#     return render_template('register.html', title='Update Post',
#                            form=form, legend='Update Post')
#
#
# @app.route("/employee/<int:id>/delete", methods=['POST'])
# def employee_delete_view(id):
#     employee = Employee.query.get_or_404(id)
#     # if employee.id != current_user:
#     #     abort(403)
#     db.session.delete(employee)
#     db.session.commit()
#     flash('Your account has been successfully deleted!', category='success')
#     return redirect(url_for('home_page_view'))
