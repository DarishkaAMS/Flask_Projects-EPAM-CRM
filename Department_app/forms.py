from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from .models import Employee


class RegisterForm(FlaskForm):

    # def validate_last_name(self, username_to_check):
    #     employee = Employee.query.filter_by(last_name=username_to_check.data).first()
    #     if employee:
    #         raise ValidationError('This last_name is already booked. Please try a different one')

    def validate_email_address(self, email_address_to_check):
        email_address = Employee.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Hmmm... I have already seen this e-mail address. Please try some other one')
    first_name = StringField(label='First Name*:', validators=[Length(min=2, max=30), DataRequired()])
    last_name = StringField(label='Last Name*:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address*:', validators=[Email(), DataRequired()])
    date_of_birth = DateField(label='Date of Birth*:', format='%Y-%m-%d')
    department = StringField(label='Department')
    salary = IntegerField(label='Salary')
    password_1 = PasswordField(label='Password*:', validators=[Length(min=8), DataRequired()])
    password_2 = PasswordField(label='Confirm Password*:', validators=[EqualTo('password_1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    email_address = StringField(label='Email Address:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')
