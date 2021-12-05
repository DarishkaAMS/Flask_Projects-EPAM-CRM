"""
form.py file of forms module for storing web form classes
"""
from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, PasswordField, StringField, SubmitField, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length

# pylint: disable=relative-beyond-top-level
from ..models.employee import Employee
from ..models.department import Department


class RegisterForm(FlaskForm):
    """
    Form for employees to create new account
    """
    first_name = StringField(label='First Name*:', validators=[Length(min=2, max=30), DataRequired()])
    last_name = StringField(label='Last Name*:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address*:', validators=[Email(), DataRequired()])
    date_of_birth = DateField(label='Date of Birth:', format='%Y-%m-%d')
    password_hash = PasswordField(label='Password*', validators=[Length(min=6), DataRequired()])
    confirm_password = PasswordField(label='Confirm Password*', validators=[
        EqualTo('password'),
        DataRequired()
    ])
    submit = SubmitField(label='Create Account')

    def validate_email_address(self, email_to_check):
        """
        Email validation function
        """
        email_address = Employee.query.filter_by(email_address=email_to_check.data).first()
        if email_address:
            raise ValidationError('Hmm... I have already seen this e-mail address. Please try some other one')


class LoginForm(FlaskForm):
    """
    Form for employees to login
    """
    email_address = StringField(label='Email:', validators=[DataRequired(), Email()])
    password_hash = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


class EmployeeForm(FlaskForm):
    """
    Form to add or edit an employee
    """
    first_name = StringField(label='First Name', validators=[DataRequired()])
    last_name = StringField(label='Last Name', validators=[DataRequired()])
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
    date_of_birth = DateField(label='Date of Birth', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


class EmployeeAssignForm(FlaskForm):
    """
    Form to assign departments and sales to employees
    """
    department = QuerySelectField(query_factory=lambda: Department.query.all(), get_label="name")
    salary = IntegerField(label='Salary')
    submit = SubmitField(label='Submit')


class EmployeeDateInfoForm(FlaskForm):
    """
    Form to assign departments and sales to employees
    """
    start_date = DateField(label='Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField(label='End Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')
