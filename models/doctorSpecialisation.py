from TransHelp import db
from datetime import datetime
from uuid import uuid4
from helpers.uuid import UuidField


class DoctorSpecialisation(db.Model):
    __tablename__ = 'doctor_has_specialisation'

    id = db.Column(UuidField, unique=True, nullable=False, default=uuid4, primary_key=True)

    doctor_id = db.Column(UuidField, db.ForeignKey('doctor.id'))
    specialisation_id = db.Column(UuidField, db.ForeignKey('specialisation.id'))

    is_main = db.Column(db.Boolean, default=True, nullable=False, unique=False)

    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
