"""
This module defines the test cases for department model
"""
# pylint: disable=import-error
from .. import db
from ..models.employee import Department
from .conftest import BaseTestCase


class TestDepartment(BaseTestCase):
    """
    Class for Department model test cases
    """
    def test_department_representation(self):
        """
        Testing if the string representation of
        department is correct
        """
        department = Department(name='Some New', head='Someone Important')
        # pylint: disable=no-member
        db.session.add(department)
        db.session.commit()
        self.assertEqual('Some New Department', repr(department))
