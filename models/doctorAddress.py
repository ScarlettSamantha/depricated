from TransHelp import db
from datetime import datetime
from uuid import uuid4
from helpers.uuid import UuidField


class DoctorAddress(db.Model):
    __tablename__ = 'doctor_has_address'

    id = db.Column(UuidField, unique=True, nullable=False, default=uuid4, primary_key=True)

    doctor_id = db.Column(UuidField, db.ForeignKey('doctor.id'))
    address_id = db.Column(UuidField, db.ForeignKey('address.id'))

    is_main = db.Column(db.Boolean, unique=False, default=True, nullable=False)

    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
