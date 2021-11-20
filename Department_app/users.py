from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25))
    last_name = db.Column(db.String(25))
    email = db.Column(db.String(50), unique=True)
    department = db.Column(db.String(15))
    password = db.Column(db.String(25))
