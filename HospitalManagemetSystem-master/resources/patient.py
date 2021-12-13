from flask_restful import Resource
from flask import request
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from models.patient import PatientModel
from schemas.patient import PatientSchema
import traceback

patient_schema = PatientSchema()
patient_list_schema = PatientSchema(many=True)



class PatientLogin(Resource):
    @classmethod
    def post(cls):
        data = patient_schema.load(request.json, partial=('email',))
        doctor = PatientModel.find_patient_by_username(data.username)
        if doctor and safe_str_cmp(doctor.password, data.password):
            access_token = create_access_token(identity=doctor.id, fresh=True)
            refresh_token = create_refresh_token(doctor.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        return {"message": "Invalid credentials!"}, 401


class Patient(Resource):
    @classmethod
    @jwt_required()
    def get(cls, patient_id: int):
        user = PatientModel.find_patient_by_id(patient_id)
        if not user:
            return {"message": "User not found."}, 404
        return patient_schema.dump(user), 200
