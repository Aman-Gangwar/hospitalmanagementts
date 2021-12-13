from typing import List
from db import db
from requests import Response, post
from models.hospital import HospitalModel
from models.doctor import DoctorModel


class PatientModel(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=False)
    username = db.Column(db.String(80), nullable=False, unique=True)
    phone_no = db.Column(db.Integer, nullable=True)
    password = db.Column(db.String(80), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey("hospitals.id"), nullable=False)
    doctor = db.relationship("DoctorModel")
    hospital = db.relationship("HospitalModel")


    @classmethod
    def find_patient_by_id(cls, _id) -> "PatientModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_patient_by_username(cls, username) -> "PatientModel":
        return cls.query.filter_by(username=username).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
