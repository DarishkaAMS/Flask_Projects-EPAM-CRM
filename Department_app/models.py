from flask_login import UserMixin

from . import bcrypt, db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


class Employee (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25))
    last_name = db.Column(db.String(25))
    date_of_birth = db.Column(db.DateTime(timezone=True), nullable=False)
    email_address = db.Column(db.String(50), nullable=False, unique=True)
    department = db.Column(db.String(15), nullable=False)
    salary = db.Column(db.Integer)
    password_hash = db.Column(db.String(length=60), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def __repr__(self):
        return f"<Employee - {self.email_address}>"


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    head = db.Column(db.String(25))
    employee = db.relationship('Employee')

    def __repr__(self):
        return f"<{self.name} Department>"
