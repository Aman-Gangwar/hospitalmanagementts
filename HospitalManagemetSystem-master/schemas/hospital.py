from ma import ma
from models.hospital import HospitalModel
from schemas.patient import PatientSchema


class HospitalSchema(ma.SQLAlchemyAutoSchema):
    patients = ma.Nested(PatientSchema, many=True)

    class Meta:
        model = HospitalModel
        load_only = ('password', 'name')
        dump_only = ('id', 'name')
        load_instance = True
        include_fk = True
