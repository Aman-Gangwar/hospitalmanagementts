from flask_restful import Resource
from flask import request
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from models.hospital import HospitalModel
from schemas.hospital import HospitalSchema
import traceback

hospital_schema = HospitalSchema()


class HospitalRegister(Resource):
    @classmethod
    def post(cls, name):
        hospital = hospital_schema.load(request.json)
        hospital.name = name
        if HospitalModel.find_hospital_by_name(name):
            return {"message": "A hospital with same name already exists."}, 400
        if HospitalModel.find_hospital_by_name(hospital.username):
            return {"message": "A hospital with same username already exists."}, 400
        try:
            hospital.save_to_db()
        except:
            traceback.print_exc()
            return {"message": "Failed to create Hospital"}, 500
        return {"message": "Hospital onboarded successfully"}, 201


class HospitalLogin(Resource):
    @classmethod
    def post(cls):
        data = hospital_schema.load(request.get_json())
        hospital = HospitalModel.find_hospital_by_username(data.username)
        if hospital and safe_str_cmp(hospital.password, data.password):
            access_token = create_access_token(identity=hospital.id, fresh=True)
            refresh_token = create_refresh_token(hospital.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": "Invalid credentials!"}, 401


class Hospital(Resource):
    @classmethod
    def get(cls, hospital_id: int):
        user = HospitalModel.find_hospital_by_id(hospital_id)
        if not user:
            return {"message": "User not found."}, 404
        return hospital_schema.dump(user), 200
