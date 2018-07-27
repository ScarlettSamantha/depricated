from os.path import exists
from uuid import uuid4
from helpers.uuid import UuidField
from TransHelp import db
from datetime import datetime
from helpers import IsRateAble, IsSearchAble, IsTagAble
from .user import User
from TransHelp import whooshee

@whooshee.register_model('title', 'content')
class Guide(IsRateAble, IsSearchAble, IsTagAble, db.Model):
    id = db.Column(UuidField, unique=True, nullable=False, default=uuid4, primary_key=True)

    title = db.Column(db.String(255), nullable=False, unique=False)

    content = db.Column(db.Text, nullable=True, unique=False)

    _requires_compilation = db.Column(db.Boolean, default=True, nullable=False, unique=False)
    _cache_file = db.Column(db.String(255), unique=True, nullable=True, default=None)
    _author_id = db.Column(UuidField, db.ForeignKey('user.id'))

    is_published = db.Column(db.Boolean, default=True, nullable=False, unique=False)

    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    _author = None

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '%s - %s' % (self.id, self.title)

    def unpublished(self) -> list:
        return self.query.filter(Guide.is_published == False).all()

    def published(self) -> list:
        return self.query.filter(Guide.is_published == True).all()

    def publish(self) -> None:
        self.is_published = True

    def unpublish(self) -> None:
        self.is_published = False

    @classmethod
    def needs_recompilation(cls):
        return cls.query.filter(cls.requires_compilation == True).all()

    def queue_recompile(self):
        self._requires_compilation = True

    def is_recompilation_needed(self) -> bool:
        return self._requires_compilation

    def compile(self):
        from helpers.guide import compile
        compile(self)

    def set_cache(self, file):
        self._cache_file = file
        self._requires_compilation = False

    def _read_cache(self):
        if self._cache_file is None or exists(self._cache_file) is False:
            raise AttributeError('cant read markdown as cache file is not set.')
        fp = open(self._cache_file, 'r')
        fp.seek(0)
        data = fp.read()
        fp.close()
        return data

    def html(self):
        if self._cache_file is None:
            self.compile()
        return self._read_cache()

    def author(self) -> User:
        if self._author is None:
            self._author = User.query.filter(User.id == self._author_id).first()
        return self._author

    def author_name(self) -> str:
        return self.author().get_display_name()