from .. import db
from flask_login import UserMixin


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    head = db.Column(db.String(25))
    employee = db.relationship('Employee')
