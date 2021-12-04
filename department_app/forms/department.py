"""
form.py file of forms module for storing web form classes
"""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms_sqlalchemy.fields import QuerySelectField

from ..models.employee import Employee
from ..models.department import Department


class DepartmentForm(FlaskForm):
    """
    Form to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    code = IntegerField('Code', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


class DepartmentUpdateForm(FlaskForm):
    """
    Form to assign departments and sales to employees
    """
    name = StringField('Name', validators=[DataRequired()])
    code = QuerySelectField(query_factory=lambda: Employee.query.all(), get_label="last_name")
    # code = QuerySelectField(query_factory=lambda: Employee.query.all(), get_label="last_name")
    submit = SubmitField(label='Submit')
