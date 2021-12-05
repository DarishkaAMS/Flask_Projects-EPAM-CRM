from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils.functions import database_exists
from flask_user import login_required, SQLAlchemyAdapter, UserManager, UserMixin
# from flask_mail import Mail

# from Flask_Projects-EPAM-CRM.config import check_config_variables_are_set, Config
from config import Config


db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()
# mail = Mail()


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
    login_manager.login_view = 'login'

    # Setup Flask-User
    from .models.employee import Employee

    db_adapter = SQLAlchemyAdapter(db,  Employee)
    user_manager = UserManager(db_adapter, app)

    # print(login_manager.user_manager, "login_manager")

    mail = Mail(app)
    # mail.init_app(app)
    migrate.init_app(app, db)

    #ADD DEPARTMENT
    from .views import user as user_blueprint
    app.register_blueprint(user_blueprint)
    from .rest import employee_api, department_api

    from .errors import forbidden_page, page_not_found, server_error_page
    app.register_error_handler(401, forbidden_page)
    app.register_error_handler(403, forbidden_page)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, server_error_page)

    api = Api(app)

    # adding the department resources
    api.add_resource(department_api.DepartmentListApi, '/api/departments')
    api.add_resource(department_api.Department, '/api/departments/<id>')

    # adding the employee resources
    api.add_resource(employee_api.EmployeeListApi, '/api/employees')
    api.add_resource(employee_api.Employee, '/api/employees/<id>')

    create_database(app)

    # msg = Message(
    #     "subject",
    #     sender="honeydummyams@gmail.com",
    #     recipients=['honeydummyams@gmail.com'],
    #     body="This is a test email I sent with Gmail and Python!"
    # )
    # mail.send(msg)

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

    assert config['MAIL_SERVER'] is not None, \
        'MAIL_SERVER is not set, ' \
        'set it in the production config file.'
    assert config['MAIL_PORT'] is not None, \
        'MAIL_PORT is not set, set the env variable APP_MAIL_USERNAME ' \
        'or MAIL_USERNAME in the production config file.'
    assert config['MAIL_USE_TLS'] is not None, \
        'MAIL_USE_TLS is not set, set the env variable APP_MAIL_PASSWORD ' \
        'or MAIL_PASSWORD in the production config file.'
    assert config['MAIL_USE_SSL'] is not None, \
        'MAIL_USE_SSL is not set, ' \
        'set it in the production config file.'
    assert config['MAIL_USERNAME'] is not None, \
        'MAIL_USERNAME is not set, set the env variable APP_MAIL_USERNAME ' \
        'or MAIL_USERNAME in the production config file.'
    assert config['MAIL_PASSWORD'] is not None, \
        'MAIL_PASSWORD is not set, set the env variable APP_MAIL_PASSWORD ' \
        'or MAIL_PASSWORD in the production config file.'
    assert config['MAIL_DEFAULT_SENDER'] is not None, \
        'MAIL_DEFAULT_SENDER is not set, set the env variable APP_MAIL_PASSWORD ' \
        'or MAIL_PASSWORD in the production config file.'
