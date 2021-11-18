from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv
import os

app = Flask(__name__, instance_relative_config=True)

ENV = 'dev'

load_dotenv()

if ENV == 'dev':
    app.debug = True
    app.secret_key = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_CREDENTIALS')}"
    # print("FFF", f"postgresql://{os.getenv('DB_CREDENTIALS')}")
    # print("FFF", app.config['SQLALCHEMY_DATABASE_URI'] == f"postgresql://{os.getenv('DB_CREDENTIALS')}")

else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    department = db.Column(db.String(25))
    salary = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, first_name, last_name, department, salary, rating, comments):
        self.first_name = first_name
        self.last_name = last_name
        self.department = department
        self.salary = salary
        self.rating = rating
        self.comments = comments

    def __str__(self):
        return f'Personal data of {self.first_name} {self.last_name}'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        department = request.form['department']
        salary = request.form['salary']
        rating = request.form['rating']
        comments = request.form['comments']
        print("SUBMIT")

        if first_name == '' or last_name == '' or department == '':
            return render_template('index.html', message='Please enter required fields')
        # if db.session.query(Employee).filter(Employee.last_name == last_name).count() == 0 or \
        #         db.session.query(Employee).filter(Employee.first_name == first_name).count() == 0:
        data = Employee(first_name, last_name, department, salary, rating, comments)
        db.session.add(data)
        db.session.commit()
        print("SEND")
            # send_mail(customer, dealer, rating, comments)
            # return render_template('success.html')
        # else:
        #     return render_template('index.html', message='We already have this employee in our database')
        return render_template('success.html', message='Your department data has been saved')


if __name__ == "__main__":
    # app.run(debug=True)
    app.run()
