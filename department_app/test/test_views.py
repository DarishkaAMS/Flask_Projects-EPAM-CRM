"""
This module defines the test cases for views
"""
# pylint: disable=cyclic-import
# pylint: disable=import-error
import http

from .. import create_app
from ..models.employee import Employee
from .conftest import BaseTestCase


class TestBaseView(BaseTestCase):
    """
    This is the class for home_page view test case
    """

    # pylint: disable=no-self-use
    def test_home_page(self):
        """
        Testing home_page accessibility without authorization
        """
        client = create_app().test_client()
        url = '/home'
        response = client.get(url)
        assert response.status_code == http.HTTPStatus.OK

    def test_register(self):
        """
        Testing login accessibility without authorization
        """
        client = create_app().test_client()
        url = '/register'
        response = client.get(url)
        assert response.status_code == http.HTTPStatus.OK

    def test_login(self):
        """
        Testing login accessibility without authorization
        """
        client = create_app().test_client()
        url = '/login'
        response = client.get(url)
        assert response.status_code == http.HTTPStatus.OK


class TestAuth(BaseTestCase):
    """
    This is the class for auth test cases
    """

    def test_success_register(self):
        """
        Testing the possibility of user registration
        """
        with create_app().test_client() as client:
            response = client.post('/register', data={
                'first_name': 'new_test',
                'last_name': 'new_test',
                'email_address': 'test@yahoo.co.uk',
                'password': 'newP@ss',
                'confirm_password': 'newP@ss'
            }, follow_redirects=True)

        # response does not depend on context, so can be tested outside the block
        assert response.status_code == http.HTTPStatus.OK

        self.assertTrue(Employee.is_authenticated)

    def test_success_login(self):
        """
        Testing the possibility of user logging in
        """
        with create_app().test_client() as client:
            response = client.post('/login', data={
                'email': 'somebody@test.com',
                'password': '1234567',
            }, follow_redirects=True)

        assert response.status_code == http.HTTPStatus.OK

        self.assertTrue(Employee.is_authenticated)
