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


class Config(object):
    """
    Base configuration
    """
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB_NAME}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """
    Testing configuration
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_CREDENTIALS')
    # print("SECRET_KEY", SECRET_KEY)
