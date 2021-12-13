from typing import List
from db import db
from requests import Response, post


class DoctorModel(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=True)
    patient = db.relationship("PatientModel", lazy="dynamic")

    @classmethod
    def find_doctor_by_name(cls, hospital_name) -> "DoctorModel":
        return cls.query.filter_by(name=hospital_name).first()

    @classmethod
    def find_doctor_by_id(cls, _id) -> "DoctorModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_doctor_by_username(cls, username) -> "DoctorModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def list_all_doctors(cls) -> List[str]:
        return [x.name for x in cls.query.all()]

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
