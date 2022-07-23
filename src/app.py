from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from requests import delete
from app import db
import sqlalchemy


# creat an instance of flask 
app = Flask(__name__)

#creating an API object
api = Api(app)

#create database
app.config['SQLALCHELY_DATABASE_URI'] = 'sqlite:///emp.db'
app.config['SQLALCHEMY_TRACK_MODIFCATION'] = False

#sqlalchemy mapper 
db = SQLAlchemy(app)

#add class
class Employee(db.Model):
    id = db.column(db.Integer, primary_key=True)
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

            emp_list.append(emp_data)
        return {"Employees" : emp_list}, 200


class AddEmploee(Resource):
    def post(self):
        if request.is_json:
            emp = Employee(firstName=request.json['FirstName'], lastName=request.json['LastName'], 
                                gender=request.json['Gender'], salary=request.json["Salary"])
            
            db.session.add(emp)
            db.session.commit()
            #retrun a json response
            return make_response(jsonify({'Id':emp.id, 'First Name': emp.firstName, 'Last Name': emp.lastName, 
                                            'Gender': emp.gender, 'Salary': emp.salary}), 201)

        else :
            return {'error':'Request must be JSON'}, 400


#for put request to localhost
class UpdateEmployee(Resource):
    def put(self, id):
        if request.is_json:
            emp = Employee.query.get(id)
            if emp is None:
                return {'error': 'not foud'}, 404
            else:
                emp.firstName = request.json['FirstName']
                emp.lastName = request.json['lastName']
                emp.gender = request.json['gender']
                emp.salary = request.json['salary']
                db.session.commit()
                return 'Updated', 200

class DeleteEmployee(Resource):
    def delete(self, id):
        emp = Employee.query.get(id)
        if emp is None:
            return {'error': 'not found'}, 404
        db.session.delete(emp)
        db.session.commit()
        return f'{id} is delete', 200

api.add_resource(GetEmployee, '/')
api.add_resource(AddEmploee, '/add')
api.add_resource(UpdateEmployee, '/update/<int:id>')
api.add_resource(DeleteEmployee, '/delete/<int:id>')


if __name__ == '__name__':
    app.run(debug=True)
    db.create_all()
