from enum import Enum
from uuid import uuid4
from helpers.uuid import UuidField
from helpers.security import check_password, generate_password, get_hash_length
from TransHelp import db
from datetime import datetime
from helpers import IsRateAble, IsSearchAble


class Permissions(Enum):
    admin = 0
    mod = 1
    user = 2


class User(IsRateAble, IsSearchAble, db.Model):
    id = db.Column(UuidField, unique=True, nullable=False, default=uuid4, primary_key=True)

    prefix = db.Column(db.String(255), unique=False, nullable=True)
    suffix = db.Column(db.String(255), unique=False, nullable=True)
    name = db.Column(db.String(255), unique=False, nullable=True)

    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(get_hash_length()), unique=False, nullable=False)
    avatar = db.Column(db.String(255), unique=False, nullable=True)

    permission_level = db.Column(db.Enum(Permissions), default=Permissions.user, nullable=False, unique=False)

    warning_note = db.Column(db.Text, unique=False, nullable=True)

    is_blocked = db.Column(db.Boolean, default=False, nullable=False, unique=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False, unique=False)
    is_trans_friendly = db.Column(db.Boolean, default=True, nullable=False, unique=False)
    has_warning = db.Column(db.Boolean, default=False, nullable=False, unique=False)

    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        if 'password' in kwargs.keys():
            self.set_password(kwargs['password'])

    def set_password(self, password):
        self.password = generate_password(password)

    def check_password(self, password):
        return check_password(self.password, password)

