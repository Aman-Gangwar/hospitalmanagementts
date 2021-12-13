from ma import ma
from models.patient import PatientModel


class PatientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PatientModel
        load_only = ('password', 'name')
        dump_only = ('id', 'name')
        include_fk = True
