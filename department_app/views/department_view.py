"""
This module represents the logic on department routes starting with:
    - /departments
    - /departments/create
    - /departments/department/<int:id>
    - /departments/department/<int:id>/update
    - /departments/department/<int:id>/delete
"""

# pylint: disable=cyclic-import
# pylint: disable=import-error
from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from flask_user import roles_required

# pylint: disable=relative-beyond-top-level
from .. import db
from ..forms.department import DepartmentForm, DepartmentUpdateForm
from ..models.department import Department

from . import user


@user.route('/departments', methods=['GET', 'POST'])
@roles_required(['hr', 'head_of_department'])
def retrieve_departments():
    """
    Handle requests to the /departments route - @roles_required(xxx)
    Retrieve all departments from the DB ordered by the Name
    """
    departments = Department.query.order_by(Department.name).all()

    return render_template('departments/departments.html', departments=departments)


@user.route('/departments/create', methods=['GET', 'POST'])
# @login_required
def create_department():
    """
    Add a department to the database
    """
    add_dep = True

    form = DepartmentForm()
    if form.validate_on_submit():
        department_to_create = Department(
            name=form.name.data,
            code=form.code.data
        )
        try:
            db.session.add(department_to_create)
            db.session.commit()
            flash('You have successfully added a new department.', category='success')

        except:
            flash('Department already exists!', category='danger')

        return redirect(url_for('user.retrieve_departments'))

    return render_template('departments/update_department.html', action='Add',
                           add_dep=add_dep, form=form)


@user.route('/departments/department/<int:id>', methods=['GET'])
# @login_required
def retrieve_department(id):
    """
    Show department
    """
    department = Department.query.get_or_404(id)

    return render_template('departments/department.html', department=department)


@user.route('/departments/department/<int:id>/update', methods=['GET', 'POST'])
# @login_required
def update_department(id):
    """
    Edit a department
    """
    add_dep = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    # form = DepartmentUpdateForm(obj=department)

    if form.validate_on_submit():
        department.name = form.name.data
        department.code = form.code.data

        print(department.code, type(department.code))
        db.session.add(department)
        db.session.commit()
        flash(f'You have successfully edited the {department.name} Department.', category='success')

        return redirect(url_for('user.retrieve_departments'))

    form.name.data = department.name
    form.code.data = department.code

    return render_template('departments/update_department.html', action="Edit",
                           add_dep=add_dep, form=form,
                           department=department)


@user.route('/departments/department/<int:id>/delete', methods=['GET', 'POST'])
# @login_required
def delete_department(id):
    """
    Delete a department from the database
    """
    department = Department.query.get_or_404(id)
    if department:
        db.session.delete(department)
        db.session.commit()
        flash(f'You have successfully deleted the {department.name} department.', category='success')

    return redirect(url_for('user.retrieve_departments'))
