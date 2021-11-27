"""
This module defines the test cases for employee model
"""
# pylint: disable=cyclic-import
from datetime import datetime

# pylint: disable=import-error
from .. import db
from ..models.employee import Employee
from .conftest import BaseTestCase


class TestEmployee(BaseTestCase):
    """
    Class for employee model test cases
    """
    def test_employee_representation(self):
        """
        Testing if the string representation of
        employee is correct
        """
        date = datetime.strptime('06/10/1998', '%m/%d/%Y').date()
        employee = Employee(
            first_name='test_first_name1',
            last_name='test_last_name1',
            email_address='test1@yahoo.co.uk',
            date_of_birth=date,
            salary=10000,
            password='test1234',
            department_id=1,
        )
        # pylint: disable=no-member
        db.session.add(employee)
        db.session.commit()
        self.assertEqual('Employee: test_username', repr(employee))
