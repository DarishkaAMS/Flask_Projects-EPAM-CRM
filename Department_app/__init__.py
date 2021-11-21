from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from os import getenv, path

from .views.views import views
from .views.auth import auth

app = Flask(__name__, instance_relative_config=True)

load_dotenv()
DB_CREDENTIALS = os.getenv('DB_CREDENTIALS')
# DB_CREDENTIALS = 'postgres:F1_Moet_2014@localhost/department_crm'
print("OS", os.getenv('DB_CREDENTIALS'))


app.debug = True
app.config['SECRET_KEY'] = 'SECRET_KEY'
# app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_CREDENTIALS')}"
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_CREDENTIALS}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# print("DATA", db)

app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')

from .models.department import Department
from .models.employee import Employee

db.create_all(app=app)
# print("FFFF", db, app)



# def create_database(app):
#     load_dotenv()
#     if not path.exists('website/' + str(DB_CREDENTIALS)):
#         db.create_all(app=app)
#         print('Created Database!', type(str({'website/' + DB_CREDENTIALS})))
#
#
# create_database(app)
