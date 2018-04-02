import enum

from TransHelp import db
from datetime import datetime
from uuid import uuid4
from helpers.uuid import UuidField
from .doctor import Doctor
from .organisation import Organisation
from .guide import Guide


class TaggableObjects(enum.Enum):
    unknown = 0
    doctor = Doctor
    organisation = Organisation
    guide = Guide


class ObjectTag(db.Model):
    __tablename__ = 'object_has_tag'

    id = db.Column(UuidField, unique=True, nullable=False, default=uuid4, primary_key=True)

    tag_id = db.Column(UuidField, db.ForeignKey('tag.id'))
    object_id = db.Column(UuidField)
    object_type = db.Column(db.Enum(TaggableObjects), default=TaggableObjects.unknown)

    is_searchable = db.Column(db.Boolean, default=True, unique=False, nullable=False)

    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
