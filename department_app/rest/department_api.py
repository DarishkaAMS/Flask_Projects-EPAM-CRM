"""
This module consists of the REST operations to work with departments
"""
# pylint: disable=cyclic-import
from flask import jsonify, request
from flask_restful import Resource

# pylint: disable=relative-beyond-top-level
from ..service import department_service


class DepartmentListApi(Resource):
    """
    Create a DepartmentListApi Resource
    """
    @staticmethod
    def get():
        """
        Called when GET request is sent
        :return: all departments in json format
        """
        return jsonify(department_service.get_all_departments())

    @staticmethod
    def post():
        """
        Called when POST request is sent
        :return: the result of the Department creation
        """
        department_json = request.json

        if not department_json:
            return {'message': 'I can\'t find that Department'}, 400
        elif department_json['name'] == '':
            return {'message': 'There is no such Department'}, 400
        try:
            department_service.add_department(
                name=department_json['name'],
                head=department_json['head']
            )
        except KeyError:
            return {'message': 'Something is wrong with the data'}, 400
        return 'Department is created successfully! ', 201


class Department(Resource):
    """
    Class for Department Resource available at '/api/departments/<id>' url
    """
    @staticmethod
    def get(id):
        """
        Called when GET request is sent
        :return: the department with a given id in json format
        """
        return jsonify(department_service.get_department_by_id(id))

    @staticmethod
    def put(id):
        """
        Called when PUT request is sent
        :return: the 'Department has been successfully updated' with status code 200
        """
        department_json = request.json
        if not department_json:
            return {'message': 'Wrong data'}, 400
        try:
            department_service.update_department(
                id,
                name=department_json['name'],
                head=department_json['head']
            )
        except KeyError:
            return {'message': 'Wrong data'}, 400
        return 'Department has been successfully updated', 200

    @staticmethod
    def patch(id):
        """
        Called when PATCH request is sent
        :return: the 'Department has been successfully updated' with status code 200
        """
        department_json = request.json
        try:
            department_service.update_department_patch(
                id,
                name=department_json.get('name'),
                description=department_json.get('description')
            )
        except KeyError:
            return {'message': 'Wrong data'}, 400
        return "Department has been successfully updated", 200

    @staticmethod
    def delete(id):
        """
        Called when DELETE request is sent
        :return: the 'Department deleted' with status code 204
        """
        department_service.delete_department(id)
        return 'Department deleted', 204
