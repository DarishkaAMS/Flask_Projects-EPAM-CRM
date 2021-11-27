"""
This module defines the test cases for department service
"""
# pylint: disable=cyclic-import
from datetime import datetime

# pylint: disable=import-error
from .. import db
from ..models.department import Department
from ..models.employee import Employee
from ..service import department_service
from ..test.conftest import BaseTestCase


class TestDepartmentService(BaseTestCase):
    """
    This is the class for department service test cases
    """

    def test_get_all_departments(self):
        """
        Testing get_all_departments by adding new departments with
        the specified parameters and checks if the count of records is equal to 2
        """
        department1 = Department(name='Some Department_1', head='Someone Important_1')
        department2 = Department(name='Some Department_2', head='Someone Important_2')
        # pylint: disable=no-member
        db.session.add(department1)
        db.session.add(department2)
        db.session.commit()
        self.assertEqual(2, len(department_service.get_all_departments()))

    def test_add_department(self):
        """
        Testing add_department by adding a new department with
        the specified parameters and checks if the count of records is equal to 1
        """
        department_service.add_department(name='New Department', head='New Important')
        self.assertEqual(1, Department.query.count())

    def test_update_department(self):
        """
        Testing update_department by adding a new department with
        the specified parameters and updates them by new records
        """
        department = Department(name='Some Department_1', head='Someone Important_1')
        # pylint: disable=no-member
        db.session.add(department)
        db.session.commit()
        department_service.update_department(1, name='New Department', head='New Important')
        department = Department.query.get(1)
        self.assertEqual('New Department', department.name)
        self.assertEqual('New Important', department.head)

    def test_delete_department(self):
        """
        Testing delete_department by adding a new department with
        the specified parameters, deletes it and checks if the count of records is equal to 1
        """
        department = Department(name='Some Department_1', head='Someone Important_1')
        # pylint: disable=no-member
        db.session.add(department)
        db.session.commit()
        department_service.delete_department(1)
        self.assertEqual(0, Department.query.count())

    def test_get_department_by_id(self):
        """
        Testing get_all_departments by adding a new department with
        the specified parameters and checks if the department id is equal to 1
        """
        department = Department(name='Some Department_1', head='Someone Important_1')
        # pylint: disable=no-member
        db.session.add(department)
        db.session.commit()
        self.assertEqual(1, department_service.get_department_by_id(1)['id'])

    def test_get_average_salary(self):
        """
        Testing the average_salary by department by adding a new department and employees
        and compares the received value with the given one.
        If they are equal then the test is successful
        """
        department = Department(name='Some Department_1', head='Someone Important_1')
        # pylint: disable=no-member
        db.session.add(department)
        date1 = datetime.strptime('10/06/1998', '%m/%d/%Y').date()
        date2 = datetime.strptime('06/10/1991', '%m/%d/%Y').date()
        employee1 = Employee(first_name='test_first_name1',
                             last_name='test_last_name1',
                             email_address='test1@yahoo.co.uk',
                             date_of_birth=date1,
                             salary=10000,
                             password='test1234',
                             department_id=1,
                             )
        employee2 = Employee(first_name='test_first_name2',
                             last_name='test_last_name2',
                             email_address='test2@yahoo.co.uk',
                             date_of_birth=date2,
                             salary=20000,
                             password='test4321',
                             department_id=1,
                             )
        db.session.add(employee1)
        db.session.add(employee2)
        db.session.commit()
        self.assertEqual(15000, department_service.get_average_salary(department.to_dict()))

    # def test_get_average_age(self):
    #     """
    #     Testing the average_age by department by adding a new department and employees
    #     and compares the received value with the given one.
    #     If they are equal then the test is successful
    #     """
    #     department = Department(name='test_department_age', head='Someone Important')
    #     # pylint: disable=no-member
    #     db.session.add(department)
    #     date1 = datetime.strptime('10/06/1998', '%m/%d/%Y').date()
    #     date2 = datetime.strptime('06/10/1991', '%m/%d/%Y').date()
    #     employee1 = Employee(
    #         username='user1',
    #         email='test1@gmail.com',
    #         first_name='test_first_name',
    #         last_name='test_last_name',
    #         password='test1234',
    #         department_id=1,
    #         salary=700,
    #         birthday=date1
    #     )
    #     employee2 = Employee(
    #         username='user2',
    #         email='test2@gmail.com',
    #         first_name='test_first_name',
    #         last_name='test_last_name',
    #         password='test1234',
    #         department_id=1,
    #         salary=500,
    #         birthday=date2
    #     )
    #     db.session.add(employee1)
    #     db.session.add(employee2)
    #     db.session.commit()
    #     self.assertEqual(26.0, department_service.get_average_age(department.to_dict()))
