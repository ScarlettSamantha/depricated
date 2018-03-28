import enum
from uuid import uuid4
from helpers.uuid import UuidField
from TransHelp import db
from datetime import datetime
from .doctor import Doctor
from .organisation import Organisation


class RateAbleObjects(enum.Enum):
    unknown = 0
    doctor = Doctor
    organisation = Organisation


class Rating(db.Model):

    id = db.Column(UuidField, unique=True, nullable=False, default=uuid4, primary_key=True)
    category = db.Column(UuidField, db.ForeignKey('rating_category.id'))
    rating = db.Column(db.Integer, unique=False, nullable=False, default=0)

    object_id = db.Column(UuidField, unique=False, nullable=False)
    object_type = db.Column(db.Enum(RateAbleObjects), nullable=False, default=RateAbleObjects.unknown)

    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
