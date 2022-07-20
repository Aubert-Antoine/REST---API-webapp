from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy


# creat an instance of flask 
app = Flask(__name__)

#creating an API object
api = Api(app)

#create database
app.config['SQLALCHELY_DATABASE_URI'] = 'sqlite:///emp.db'
app.config['SQLALCHEMY_TRACK_MODIFCATION'] = False

#sqlalchemy mapper 
db = sqlalchemy(app)

#add class
class Employee(db.Model):
    id = db.column(db.Interger, primary_key=True)
    firstName = db.Column(db.String(80), nullable=False)
    lastName = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    salary = db.Column(db.Float)

    def __repr__(self) -> str:
        return "{} - {} - {} -{}".format(self.firstName, self.lastName, self.gender, self.salary)


class GetEmployee(Resource):
    def get(self):
        employee = Employee.query.all()
        emp_list = []
        for emp in employee:
            emp_data = {'ID' : emp.id, 'FirstName' : emp.firstName, 'LastName' : emp.lastName,
             'Gender' : emp.gender, 'Salary' : emp.Salary }

            emp_list(emp_data)