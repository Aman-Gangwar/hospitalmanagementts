from db import db
from requests import Response, post


class HospitalModel(db.Model):
    __tablename__ = "hospitals"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=True)
    patient = db.relationship("PatientModel", lazy="dynamic")
    @classmethod
    def find_hospital_by_name(cls, hospital_name) -> "HospitalModel":
        return cls.query.filter_by(name=hospital_name).first()

    @classmethod
    def find_hospital_by_id(cls, _id) -> "HospitalModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_hospital_by_username(cls, username) -> "HospitalModel":
        return cls.query.filter_by(username=username).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
