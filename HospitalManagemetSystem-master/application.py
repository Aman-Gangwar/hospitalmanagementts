from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

load_dotenv(".env", verbose=True)
from db import db
from resources.hospital import Hospital, HospitalRegister, HospitalLogin
from resources.doctor import Doctor, DoctorLogin, DoctorRegister, DoctorList
from ma import ma
from marshmallow import ValidationError
import os

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['PROPAGATE_EXCEPTIONS'] = True
application.secret_key = 'tverma'
api = Api(application)
db.init_app(application)
ma.init_app(application)

@application.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(application)

@application.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


api.add_resource(Hospital, "/hospital/<int:id>")
api.add_resource(HospitalRegister, "/hospital/register/<string:name>")
api.add_resource(HospitalLogin, "/hospital/login")
api.add_resource(Doctor, "/doctor/<int:id>")
api.add_resource(DoctorRegister, "/doctor/register")
api.add_resource(DoctorLogin, "/doctor/login")
api.add_resource(DoctorList, "/doctor/all")


if __name__ == "__main__":
    application.run(port=5000, debug=True)
