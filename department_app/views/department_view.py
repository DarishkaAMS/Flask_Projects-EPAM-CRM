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
from .. import create_app, db
from ..forms.department import DepartmentForm
from ..models.department import Department

from . import user

app = create_app()


@user.route('/departments', methods=['GET', 'POST'])
@roles_required(['hr', 'head_of_department'])
def retrieve_departments():
    """
    Handle requests to the /departments route - @roles_required(xxx)
    Retrieve all departments from the DB ordered by the Name
    """
    departments = Department.query.order_by(Department.name).all()
    app.logger.info(f'User visited /departments page')
    return render_template('departments/departments.html', departments=departments)


@user.route('/departments/create', methods=['GET', 'POST'])
@roles_required(['hr'])
def create_department():
    """
    Handle requests to the /departments/create route - @roles_required(xxx)
    Add an department to the DB using DepartmentForm and required checks
    Redirect to departments page after successful department creation
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
            app.logger.info(f'Department with ID {department_to_create.id} has been created')
            flash('You have successfully added a new department.', category='success')

        except:
            flash('Department already exists!', category='danger')

        return redirect(url_for('user.retrieve_departments'))

    return render_template('departments/update_department.html', action='Add',
                           add_dep=add_dep, form=form)


@user.route('/departments/department/<int:id>', methods=['GET'])
@roles_required(['hr', 'head_of_department'])
def retrieve_department(id):
    """
    Handle requests to the /departments/department/<int:id> route - @roles_required(xxx)
    Retrieve the department with specified ID from the DB
    """
    department = Department.query.get_or_404(id)
    app.logger.info(f'Employee with ID {department.id} has been retrieved')
    return render_template('departments/department.html', department=department)


@user.route('/departments/department/<int:id>/update', methods=['GET', 'POST'])
@roles_required(['head_of_department'])
def update_department(id):
    """
    Handle requests to the /departments/department/<int:id>/update route - @roles_required(xxx)
    Update an department with specified ID
    """
    add_dep = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    # form = DepartmentUpdateForm(obj=department)

    if form.validate_on_submit():
        department.name = form.name.data
        department.code = form.code.data
        db.session.add(department)
        db.session.commit()
        app.logger.info(f'Department with ID {department.id} is updated')
        flash(f'You have successfully edited the {department.name} Department.', category='success')

        return redirect(url_for('user.retrieve_departments'))

    form.name.data = department.name
    form.code.data = department.code

    app.logger.info(f'Employee with ID {department.id} is about to be updated')
    return render_template('departments/update_department.html', action="Edit",
                           add_dep=add_dep, form=form,
                           department=department)


@user.route('/departments/department/<int:id>/delete', methods=['GET', 'POST'])
@roles_required(['head_of_department'])
def delete_department(id):
    """
    Handle requests to the /departments/department/<int:id>/delete route - @roles_required(xxx)
    Delete an department with specified ID redirecting to the home page.
    """
    department = Department.query.get_or_404(id)
    if department:
        db.session.delete(department)
        db.session.commit()
        flash(f'You have successfully deleted the {department.name} department.', category='success')
        app.logger.info(f'Employee with ID {department.id} is deleted')

    return redirect(url_for('user.retrieve_departments'))
