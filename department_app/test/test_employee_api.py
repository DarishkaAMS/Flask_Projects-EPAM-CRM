"""
This module defines the test cases for employee api
"""
# pylint: disable=cyclic-import
import http
import json

# pylint: disable=import-error
from unittest.mock import patch

from .. import create_app
from .conftest import BaseTestCase


class TestEmployeeApi(BaseTestCase):
    """
    This is the class for employee api test cases
    """

    # pylint: disable=no-self-use
    def test_get(self):
        """
        Testing the get request to /api/employees.
        It should return the status code 200
        """
        client = create_app().test_client()
        response = client.get('/api/employees')

        assert response.status_code == http.HTTPStatus.OK

    @patch('department_app.service.employee_service.get_all_employees',
           autospec=True, return_value=[])
    def test_get_with_mock_db(self, mock_db_call):
        """
        Testing the get request to /api/employees with mock db.
        It should return the status code 200 and an empty list
        """
        client = create_app().test_client()
        response = client.get('/api/employees')

        mock_db_call.assert_called_once()
        assert response.status_code == http.HTTPStatus.OK
        assert len(response.json) == 0

    def test_get_employee(self):
        """
        Testing the get request to /api/employees/<id>
        It should return the status code 200
        """
        client = create_app().test_client()
        url = '/api/employees/6'
        response = client.get(url)
        assert response.status_code == http.HTTPStatus.OK

    def test_post(self):
        """
        Testing the post request to /api/employees.
        It should return the status code 201
        """
        client = create_app().test_client()
        # data should be changed before calling the test
        data = {
            'first_name': 'new_test',
            'last_name': 'new_test',
            'email_address': 'test@yahoo.co.uk',
            'date_of_birth': '10/06/1998',
            'salary': '10000',
            'password': 'test1234',
            'department_id': 3,
        }
        response = client.post('/api/employees', data=json.dumps(data),
                               content_type='application/json')
        assert response.status_code == http.HTTPStatus.CREATED

    def test_post_with_mock_db(self):
        """
        Testing the post request to /api/employees with mock db
        """
        with patch('department_app.db.session.add', autospec=True) as mock_session_add, \
                patch('department_app.db.session.commit', autospec=True) as mock_session_commit:
            client = create_app().test_client()
            data = {
                'first_name': 'new_test',
                'last_name': 'new_test',
                'email_address': 'test@yahoo.co.uk',
                'date_of_birth': '10/06/1998',
                'salary': '10000',
                'password': 'test1234',
                'department_id': 3,
            }
            client.post('/api/employees', data=json.dumps(data),
                        content_type='application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()

    def test_put(self):
        """
        Testing the put request to /api/employees/<id> .
        It should return the status code 200
        """
        client = create_app().test_client()
        url = '/api/employees/6'
        data = {
            'first_name': 'new_test',
            'last_name': 'new_test',
            'email_address': 'test@yahoo.co.uk',
            'date_of_birth': '10/06/1998',
            'salary': '10000',
            'password': 'test1234',
            'department_id': 3,
        }
        response = client.put(url, data=json.dumps(data),
                              content_type='application/json')
        assert response.status_code == http.HTTPStatus.OK

    def test_get_employees_born_on(self):
        """
        Testing the get request to /api/employees?date='date'
        where date is a birthday of existing employee.
        It should return the status code 200
        """
        client = create_app().test_client()
        url = '/api/employees?date=\'10/06/1998\''
        response = client.get(url)
        assert response.status_code == http.HTTPStatus.OK

    def test_get_employees_born_between(self):
        """
        Testing the get request to /api/employees?start_date='start_date'&end_date='end_date'
        It should return the status code 200
        """
        client = create_app().test_client()
        url = '/api/employees?start_date=\'12/13/1971\'&end_date=\'12/13/1991\''
        response = client.get(url)
        assert response.status_code == http.HTTPStatus.OK
