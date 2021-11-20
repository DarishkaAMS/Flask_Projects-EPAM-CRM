from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv
import os


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    ENV = 'dev'

    from .views.views import views
    from .views.auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    load_dotenv()

    if ENV == 'dev':
        app.debug = True
        app.config['SECRET_KEY'] = 'SECRET_KEY'
        app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_CREDENTIALS')}"

    else:
        app.debug = False
        app.config['SQLALCHEMY_DATABASE_URI'] = ''

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    return app
