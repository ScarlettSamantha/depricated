from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID
from TransHelp import db
import uuid

class Uuid():
    LENGTH_WITH_DASHES = 36
    LENGTH_WITHOUT_DASHES = 32
    LENGTH_HEX = 16

    @classmethod
    def length(cls):
        return cls.LENGTH_WITH_DASHES


class UuidField(TypeDecorator):
    """Platform-independent GUID type.

    Uses Postgresql's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                # Add this for support so we can just throw a model in it.
                if isinstance(value, db.Model):
                    if hasattr(value, '__ID_FIELD__'):
                        value = getattr(value, getattr(value, '__ID_FIELD__'))
                    elif hasattr(value, 'id'):
                        value = getattr(value, 'id')
                return "%.32x" % uuid.UUID(hex=value).__int__()
            else:
                # hexstring
                return "%.32x" % value.__int__()

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)
