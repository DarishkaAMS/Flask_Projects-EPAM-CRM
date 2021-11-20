from . import db
from flask_login import UserMixin


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    head = db.Column(db.String(25))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25))
    last_name = db.Column(db.String(25))
    # date_of_birth = db.Column(db.String(25))
    email = db.Column(db.String(50), unique=True)
    department = db.Column(db.String(15))
    salary = db.Column(db.Integer)
    password = db.Column(db.String(25))
