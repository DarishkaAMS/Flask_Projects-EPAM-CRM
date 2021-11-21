from .. import db
from flask_login import UserMixin


class Employee (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25))
    last_name = db.Column(db.String(25))
    date_of_birth = db.Column(db.DateTime(timezone=True))
    email = db.Column(db.String(50), unique=True)
    department = db.Column(db.String(15))
    salary = db.Column(db.Integer)
    password = db.Column(db.String(25))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
