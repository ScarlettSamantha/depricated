from uuid import uuid4
from helpers.uuid import UuidField
from TransHelp import db
from datetime import datetime


class Address(db.Model):
    id = db.Column(UuidField, unique=True, nullable=False, default=uuid4, primary_key=True)

    line1 = db.Column(db.String(255), unique=False, nullable=True)
    line2 = db.Column(db.String(255), unique=False, nullable=True)
    line3 = db.Column(db.String(255), unique=False, nullable=True)
    city = db.Column(db.String(255), unique=False, nullable=True)
    postcode = db.Column(db.String(255), unique=False, nullable=True)
    province = db.Column(db.String(255), unique=False, nullable=True)
    country = db.Column(db.String(3), unique=False, nullable=False)
    phone = db.Column(db.String(255), unique=False, nullable=True)
    fax = db.Column(db.String(255), unique=False, nullable=True)

    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
