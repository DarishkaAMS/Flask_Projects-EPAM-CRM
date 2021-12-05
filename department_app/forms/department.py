"""
File of Department forms module for storing web form classes:
 - DepartmentForm to add or edit a department
 - DepartmentUpdateForm to assign departments and sales to employees
"""

from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField

from ..models.employee import Employee


class DepartmentForm(FlaskForm):
    """
    Form to add or edit a department
    """
    name = StringField(label='Name', validators=[DataRequired()])
    code = IntegerField(label='Code', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


class DepartmentUpdateForm(FlaskForm):
    """
    Form to assign departments and sales to employees
    """
    name = StringField(label='Name', validators=[DataRequired()])
    code = QuerySelectField(query_factory=lambda: Employee.query.all(), get_label="last_name")
    submit = SubmitField(label='Submit')
