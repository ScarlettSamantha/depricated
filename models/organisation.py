from uuid import uuid4
from helpers.uuid import UuidField
from TransHelp import db
from datetime import datetime
from helpers import IsTagAble, IsRateAble, IsSearchAble
from .organisationAddress import OrganisationAddress
from .address import Address

import pycountry
from TransHelp import whooshee

@whooshee.register_model('name', 'email', 'phone', 'website')
class Organisation(IsTagAble, IsRateAble, IsSearchAble, db.Model):
    id = db.Column(UuidField, unique=True, nullable=False, default=uuid4, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)

    email = db.Column(db.String(255), unique=False, nullable=True)
    phone = db.Column(db.String(255), unique=False, nullable=True)
    website = db.Column(db.String(255), unique=False, nullable=True)

    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    _address = None

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '%s-%s' % (self.id, self.name)

    def address(self):
        if self._address is None:
            self._address = Address.query.join(OrganisationAddress)\
                .filter(Address.id == OrganisationAddress.address_id)\
                .filter(OrganisationAddress.organisation_id == self.id)\
                .first()
        return self._address

    def country_formatted(self):
        c = pycountry.countries.get(alpha_2=self.address().country)
        try:
            return c.offical_name
        except AttributeError:
            return c.name

    def country(self):
        return self.country_formatted()

    def country_code(self):
        return self.address().country