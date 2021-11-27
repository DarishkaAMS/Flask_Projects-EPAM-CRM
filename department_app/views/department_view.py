"""
This module represents the logic on routes starting with /departments
"""

# pylint: disable=cyclic-import
# pylint: disable=import-error
from flask import render_template, redirect, url_for, flash
from flask_login import login_required

# pylint: disable=relative-beyond-top-level
from .. import db
from ..models.department import Department
from ..forms.department import DepartmentForm

from . import user


@user.route('/departments', methods=['GET', 'POST'])
@login_required
def show_departments():
    """
    Show all departments
    """
    departments = Department.query.order_by(Department.name).all()

    return render_template('departments/departments.html', departments=departments)


@user.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    """
    Add a department to the database
    """
    add_dep = True

    form = DepartmentForm()
    if form.validate_on_submit():
        department_to_create = Department(
            name=form.name.data,
            head=form.head.data
        )
        try:
            db.session.add(department_to_create)
            db.session.commit()
            flash('You have successfully added a new department.', category='success')

        except:
            flash('Department already exists!', category='danger')

        return redirect(url_for('user.show_departments'))

    return render_template('departments/department.html', action='Add',
                           add_dep=add_dep, form=form)


@user.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    """
    Edit a department
    """
    add_dep = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.head = form.head.data

        db.session.commit()
        flash(f'You have successfully edited the {department.name} Department.', category='success')

        return redirect(url_for('user.show_departments'))

    form.name.data = department.name
    form.head.data = department.head

    return render_template('departments/department.html', action="Edit",
                           add_dep=add_dep, form=form,
                           department=department)


@user.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    """
    Delete a department from the database
    """
    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash(f'You have successfully deleted the {department.name} department.', category='success')

    return redirect(url_for('user.show_departments'))
