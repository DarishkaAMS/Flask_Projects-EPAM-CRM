"""Specify configurations"""
from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')
SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')

POSTGRES_USERNAME = os.environ.get('POSTGRES_USERNAME')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_DB_NAME = os.environ.get('POSTGRES_DB_NAME')

MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_PORT = os.environ.get('MAIL_PORT')
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL')
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

#MOVED TO INIT
# def check_config_variables_are_set(config):
#     assert config['SECRET_KEY'] is not None, \
#         'SECRET_KEY is not set, set it in the production config file.'
#     assert config['SECURITY_PASSWORD_SALT'] is not None, \
#         'SECURITY_PASSWORD_SALT is not set, ' \
#         'set it in the production config file.'
#
#     # assert config['POSTGRES_USERNAME'] is not None, \
#     #     'POSTGRES_USERNAME is not set, ' \
#     #     'set it in the production config file.'
#     # assert config['POSTGRES_PASSWORD'] is not None, \
#     #     'POSTGRES_PASSWORD is not set, set it in the production config file.'
#     # assert config['POSTGRES_HOST'] is not None, \
#     #     'POSTGRES_HOST is not set, ' \
#     #     'set it in the production config file.'
#     # assert config['POSTGRES_DB_NAME'] is not None, \
#     #     'POSTGRES_DB_NAME is not set, set it in the production config file.' \
#     #     'set it in the production config file.'
#     # assert config['POSTGRES_HOST_PORT'] is not None, \
#     #     'POSTGRES_HOST_PORT is not set, ' \
#     #     'set it in the production config file.'
#
#     assert config['MAIL_DEFAULT_SENDER'] is not None, \
#         'MAIL_DEFAULT_SENDER is not set, ' \
#         'set it in the production config file.'
#
#     # assert config['POSTGRES_USERNAME'] is not None,\
#     #        'POSTGRES_USERNAME is not set, '\
#     #        'set it in the production config file.'
#     # assert config['MAIL_USERNAME'] is not None, \
#     #     'MAIL_USERNAME is not set, set the env variable APP_MAIL_USERNAME ' \
#     #     'or MAIL_USERNAME in the production config file.'
#     # assert config['MAIL_PASSWORD'] is not None, \
#     #     'MAIL_PASSWORD is not set, set the env variable APP_MAIL_PASSWORD ' \
#     #     'or MAIL_PASSWORD in the production config file.'
#
#     print("Success!!!")
#

class Config(object):
    """
    Base configuration
    """
    SECRET_KEY = SECRET_KEY
    SECURITY_PASSWORD_SALT = SECURITY_PASSWORD_SALT
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB_NAME}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = MAIL_SERVER
    MAIL_PORT = MAIL_PORT
    MAIL_USE_TLS = MAIL_USE_TLS
    MAIL_USE_SSL = MAIL_USE_SSL
    MAIL_USERNAME = MAIL_USERNAME
    MAIL_PASSWORD = MAIL_PASSWORD
    MAIL_DEFAULT_SENDER = MAIL_DEFAULT_SENDER


class TestingConfig(Config):
    """
    Testing configuration
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_CREDENTIALS')
    # print("SECRET_KEY", SECRET_KEY)
