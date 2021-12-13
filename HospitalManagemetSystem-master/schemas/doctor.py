from ma import ma
from models.doctor import DoctorModel
from schemas.patient import PatientSchema

class DoctorSchema(ma.SQLAlchemyAutoSchema):
    patients = ma.Nested(PatientSchema, many=True)
    class Meta:
        model = DoctorModel
        load_only = ('password',)
        dump_only = ('id', )
        include_fk = True
        load_instance = True
