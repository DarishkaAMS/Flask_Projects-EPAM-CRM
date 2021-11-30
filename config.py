"""Specify configurations"""
from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')
POSTGRES_USERNAME = os.environ.get('POSTGRES_USERNAME')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_DB_NAME = os.environ.get('POSTGRES_DB_NAME')
SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')


def _check_config_variables_are_set(config):
    assert config['MAIL_USERNAME'] is not None,\
           'MAIL_USERNAME is not set, set the env variable APP_MAIL_USERNAME '\
           'or MAIL_USERNAME in the production config file.'
    assert config['MAIL_PASSWORD'] is not None,\
           'MAIL_PASSWORD is not set, set the env variable APP_MAIL_PASSWORD '\
           'or MAIL_PASSWORD in the production config file.'

    assert config['SECRET_KEY'] is not None,\
           'SECRET_KEY is not set, set it in the production config file.'
    assert config['SECURITY_PASSWORD_SALT'] is not None,\
           'SECURITY_PASSWORD_SALT is not set, '\
           'set it in the production config file.'

    assert config['SQLALCHEMY_DATABASE_URI'] is not None,\
           'SQLALCHEMY_DATABASE_URI is not set, '\
           'set it in the production config file.'

    if os.environ['APP_SETTINGS'] == 'project.config.ProductionConfig':
        assert config['STRIPE_SECRET_KEY'] is not None,\
               'STRIPE_SECRET_KEY is not set, '\
               'set it in the production config file.'
        assert config['STRIPE_PUBLISHABLE_KEY'] is not None,\
               'STRIPE_PUBLISHABLE_KEY is not set, '\
               'set it in the production config file.'


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
    MAIL_DEFAULT_SENDER = MAIL_DEFAULT_SENDER


class TestingConfig(Config):
    """
    Testing configuration
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_CREDENTIALS')
    # print("SECRET_KEY", SECRET_KEY)
