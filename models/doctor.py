import pycountry
from uuid import uuid4
from helpers.uuid import UuidField
from TransHelp import db
from datetime import datetime
from helpers import IsTagAble, IsRateAble, IsSearchAble
from .organisation import Organisation


class Doctor(IsTagAble, IsRateAble, IsSearchAble, db.Model):
    id = db.Column(UuidField, unique=True, nullable=False, default=uuid4, primary_key=True)

    prefix = db.Column(db.String(255), unique=False, nullable=False)
    suffix = db.Column(db.String(255), unique=False, nullable=False)
    name = db.Column(db.String(255), unique=False, nullable=False)

    email = db.Column(db.String(255), unique=False, nullable=True)
    phone = db.Column(db.String(255), unique=False, nullable=True)
    note = db.Column(db.Text, unique=False, nullable=True)
    picture = db.Column(db.String(255), unique=False, nullable=True, default=None)
    website = db.Column(db.String(255), unique=False, nullable=True)

    organisation_id = db.Column(UuidField, db.ForeignKey('organisation.id'))

    is_approved = db.Column(db.Boolean, default=True, nullable=False, unique=False)
    is_blocked = db.Column(db.Boolean, default=False, nullable=False, unique=False)
    is_trans_friendly = db.Column(db.Boolean, default=True, nullable=False, unique=False)
    has_warning = db.Column(db.Boolean, default=False, nullable=False, unique=False)

    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    _organisation = None

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def organisation(self) -> Organisation:
        if self._organisation is None:
            self._organisation = Organisation.query.filter(Organisation.id == self.organisation_id).first()
        return self._organisation

    def country(self):
        return self.organisation().country_formatted()

    def country_code(self):
        return self.organisation().address().country


