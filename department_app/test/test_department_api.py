"""
This module defines the test cases for department api
"""
# pylint: disable=cyclic-import
import http
import json

# pylint: disable=import-error
from dataclasses import dataclass
from unittest.mock import patch

from .. import db, create_app
from ..models.department import Department
from .conftest import BaseTestCase


@dataclass
class FakeDepartment:
    """
    It is the needed Department for test_put_with_mock_db as return value in mocked_query
    """
    name = 'Some Department'
    head = 'Someone Important'


class TestDepartmentApi(BaseTestCase):
    """
    This is the class for department api test cases
    """

    # pylint: disable=no-self-use
    def test_get(self):
        """
        Testing the get request to /api/departments.
        It should return the status code 200
        """
        client = create_app().test_client()
        response = client.get('/api/departments')

        assert response.status_code == http.HTTPStatus.OK

    def test_get_department(self):
        """
        Testing the get request to /api/departments/<id>
        It should return the status code 200
        """
        client = create_app().test_client()
        url = '/api/departments/2'
        response = client.get(url)
        assert response.status_code == http.HTTPStatus.OK

    @patch('department_app.service.department_service.get_all_departments',
           autospec=True, return_value=[])
    def test_get_with_mock_db(self, mock_db_call):
        """
        Testing the get request to /api/departments with mock db.
        It should return the status code 200 and an empty list
        """
        client = create_app().test_client()
        response = client.get('/api/departments')

        mock_db_call.assert_called_once()
        assert response.status_code == http.HTTPStatus.OK
        assert len(response.json) == 0

    def test_post(self):
        """
        Testing the post request to /api/departments.
        It should return the status code 201
        """
        client = create_app().test_client()
        # data should be changed before calling the test
        data = {
            'name': 'Some Department_1',
            'head ': 'Someone  Important_1'
        }
        response = client.post('/api/departments', data=json.dumps(data),
                               content_type='application/json')
        assert response.status_code == http.HTTPStatus.CREATED

    def test_post_with_mock_db(self):
        """
        Testing the post request to /api/departments with mock db
        """
        with patch('department_app.db.session.add',
                   autospec=True) as mock_session_add, \
                patch('department_app.db.session.commit',
                      autospec=True) as mock_session_commit:
            client = create_app().test_client()
            data = {
                'name': 'Some Department_2',
                'head ': 'Someone  Important_2'
            }
            client.post('/api/departments', data=json.dumps(data),
                        content_type='application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()

    def test_put(self):
        """
        Testing the put request to /api/departments/<id>
        It should return the status code 200
        """
        department = Department(name='Some Department_1', head='Someone  Important_1')
        # pylint: disable=no-member
        db.session.add(department)
        db.session.commit()
        client = create_app().test_client()
        url = '/api/departments/1'
        data = {
            'name': 'Update Some Department_1',
            'head': 'Update Someone Important_1'
        }
        response = client.put(url, data=json.dumps(data),
                              content_type='application/json')
        assert response.status_code == http.HTTPStatus.OK

    def test_put_with_mock_db(self):
        """
        Testing the put request to /api/departments/<id> with mock db
        """
        # create department
        department = Department(name='Some Department_1', head='Someone  Important_1')
        # pylint: disable=no-member
        db.session.add(department)
        db.session.commit()

        # update department
        with patch('department_app.service.department_service.get_department_by_id') \
                as mocked_query, \
                patch('department_app.db.session.add', autospec=True) as mock_session_add, \
                patch('department_app.db.session.commit', autospec=True) as mock_session_commit:
            mocked_query.return_value = FakeDepartment()
            client = create_app().test_client()
            url = '/api/departments/1'
            data = {
                'name': 'Update Some Department_1',
                'head': 'Update Someone Important_1'
            }
            client.put(url, data=json.dumps(data),
                       content_type='application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()

    def test_delete(self):
        """
        Testing the delete request to /api/departments/<id>
        It should return the status code 204 (NO_CONTENT)
        """
        department = Department(name='Some Department_1', head='Someone  Important_1')
        # pylint: disable=no-member
        db.session.add(department)
        db.session.commit()

        client = create_app().test_client()
        url = '/api/departments/1'
        response = client.delete(url)
        assert response.status_code == http.HTTPStatus.NO_CONTENT
