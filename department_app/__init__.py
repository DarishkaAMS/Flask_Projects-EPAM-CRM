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
# from Flask_Projects-EPAM-CRM.config import check_config_variables_are_set, Config
from config import Config


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

    check_config_variables_are_set(app.config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail = Mail(app)
    migrate.init_app(app, db)

    #ADD DEPARTMENT
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

    return app


def create_database(app):
    """
    Create DB using configs
    """
    if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
        # raise Error ?????
        print('There is no such Database')

    try:
        db.create_all(app=app)
    except Exception as e:
        return f'The error has occurred while trying to create DB - {e}'


def check_config_variables_are_set(config):
    assert config['SECRET_KEY'] is not None, \
        'SECRET_KEY is not set, set it in the production config file.'
    assert config['SECURITY_PASSWORD_SALT'] is not None, \
        'SECURITY_PASSWORD_SALT is not set, ' \
        'set it in the production config file.'

    assert config['SQLALCHEMY_DATABASE_URI'] is not None, \
        'SQLALCHEMY_DATABASE_URI is not set, ' \
        'set it in the production config file.'

    # assert config['MAIL_DEFAULT_SENDER'] is not None, \
    #     'MAIL_DEFAULT_SENDER is not set, ' \
    #     'set it in the production config file.'
    # assert config['MAIL_USERNAME'] is not None, \
    #     'MAIL_USERNAME is not set, set the env variable APP_MAIL_USERNAME ' \
    #     'or MAIL_USERNAME in the production config file.'
    # assert config['MAIL_PASSWORD'] is not None, \
    #     'MAIL_PASSWORD is not set, set the env variable APP_MAIL_PASSWORD ' \
    #     'or MAIL_PASSWORD in the production config file.'

    print("Success!!!")