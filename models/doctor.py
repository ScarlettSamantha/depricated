from uuid import uuid4
from helpers.uuid import UuidField
from TransHelp import db
from datetime import datetime
from helpers import IsTagAble, IsRateAble, IsSearchAble


class Doctor(IsTagAble, IsRateAble, IsSearchAble, db.Model):
    id = db.Column(UuidField, unique=True, nullable=False, default=uuid4, primary_key=True)

    name = db.Column(db.String(255), unique=False, nullable=False)

    email = db.Column(db.String(255), unique=False, nullable=True)
    phone = db.Column(db.String(255), unique=False, nullable=True)
    note = db.Column(db.Text, unique=False, nullable=True)
    picture = db.Column(db.String(255), unique=False, nullable=True, default=None)
    website = db.Column(db.String(255), unique=False, nullable=True)

    is_approved = db.Column(db.Boolean, default=True, nullable=False, unique=False)
    is_blocked = db.Column(db.Boolean, default=False, nullable=False, unique=False)
    is_trans_friendly = db.Column(db.Boolean, default=True, nullable=False, unique=False)
    has_warning = db.Column(db.Boolean, default=False, nullable=False, unique=False)

    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)


