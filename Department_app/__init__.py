from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv
import os

from .views.views import views
from .views.auth import auth

app = Flask(__name__, instance_relative_config=True)

load_dotenv()
app.debug = True
app.config['SECRET_KEY'] = 'SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_CREDENTIALS')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

print("DATA", db)

app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')
