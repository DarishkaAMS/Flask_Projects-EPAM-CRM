"""
form.py file of forms module for storing web form classes
"""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from ..models.employee import Employee
from ..models.department import Department


class DepartmentForm(FlaskForm):
    """
    Form to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    head = StringField('Head', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


