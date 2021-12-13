from flask_restful import Resource
from flask import request
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from models.doctor import DoctorModel
from schemas.doctor import DoctorSchema
import traceback

doctor_schema = DoctorSchema()
doctor_list_schema = DoctorSchema(many=True)


class DoctorRegister(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        doctor = doctor_schema.load(request.get_json())
        if DoctorModel.find_doctor_by_username(doctor.username):
            return {"message": "A doctor with same username already exists."}, 400
        try:
            doctor.save_to_db()
        except:
            traceback.print_exc()
            return {"message": "Failed to create doctor"}, 500
        return {"message": "doctor onboarded successfully"}, 201


class DoctorLogin(Resource):
    @classmethod
    def post(cls):
        data = doctor_schema.load(request.get_json(), partial=('name',))
        doctor = DoctorModel.find_doctor_by_username(data.username)
        if doctor and safe_str_cmp(doctor.password, data.password):
            access_token = create_access_token(identity=doctor.id, fresh=True)
            refresh_token = create_refresh_token(doctor.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        return {"message": "Invalid credentials!"}, 401


class Doctor(Resource):
    @classmethod
    @jwt_required()
    def get(cls, doctor_id: int):
        user = DoctorModel.find_doctor_by_id(doctor_id)
        if not user:
            return {"message": "User not found."}, 404
        return doctor_schema.dump(user), 200


class DoctorList(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        return {"doctors": DoctorModel.list_all_doctors()}, 200
