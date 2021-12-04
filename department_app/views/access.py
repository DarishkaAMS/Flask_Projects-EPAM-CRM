# from functools import wraps
# from flask import url_for, request, redirect, session
# from .employee_view import Employee
#
#
# def requires_access_level(access_level):
#     def decorator(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             confirmed_employee
#             confirmed_employee = Employee.query.filter_by(email_address=session['email_address']).first_or_404()
#
#             # employee = Employee.find_by_email(session['email_address'])
#             # if not session.get('email_address'):
#             #     return redirect(url_for('user.login_page'))
#             # elif not employee.allowed(access_level):
#             if not confirmed_employee.allowed(access_level):
#                 return redirect(url_for('user.home', message="You do not have access to that page. Sorry!"))
#             return f(*args, **kwargs)
#         return decorated_function
#     return decorator
