from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils.functions import database_exists

from dotenv import load_dotenv
from config import Config
# from ..config import _check_config_variables_are_set


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

    # _check_config_variables_are_set(app.config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail = Mail(app)
    migrate.init_app(app, db)

    from .views import user as user_blueprint
    app.register_blueprint(user_blueprint)
    from .rest import employee_api, department_api

    # ADD BLUEPRINTS
    # from project.main.views import main_blueprint
    # from project.user.views import user_blueprint
    # app.register_blueprint(main_blueprint)
    # app.register_blueprint(user_blueprint)

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

    return app


def create_database(app):
    """
    Create DB using configs
    """
    if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
        print('There is no such Database')

    try:
        db.create_all(app=app)
    except Exception as e:
        return f'The error has occurred while trying to create DB - {e}'

