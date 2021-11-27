from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv
from config import Config
from os import path

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()


def create_app():
    """
    Create flask application
    :return: the app instance
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from .views import user as user_blueprint
    app.register_blueprint(user_blueprint)
    from .rest import employee_api, department_api

    api = Api(app)

    # adding the department resources
    api.add_resource(department_api.DepartmentListApi, '/api/departments')
    api.add_resource(department_api.Department, '/api/departments/<id>')

    # adding the employee resources
    api.add_resource(employee_api.EmployeeListApi, '/api/employees')
    api.add_resource(employee_api.Employee, '/api/employees/<id>')

    from .models.department import Department
    from .models.employee import Employee

    create_database(app)
    print('CREATE EXISTS!', db)

    return app


def create_database(app):
    # if not path.exists('website/' + DB_NAME):
    #     db.create_all(app=app)
    print('Created EXISTS!', db)
    db.create_all(app=app)
    print('Created Database!', db)
