from TransHelp import db
from datetime import datetime
from uuid import uuid4
from helpers.uuid import UuidField


class OrganisationAddress(db.Model):
    __tablename__ = 'organisation_has_address'

    id = db.Column(UuidField, unique=True, nullable=False, default=uuid4, primary_key=True)

    organisation_id = db.Column(UuidField, db.ForeignKey('organisation.id'))
    address_id = db.Column(UuidField, db.ForeignKey('address.id'))

    is_main = db.Column(db.Boolean, default=True, nullable=False, unique=False)

    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
