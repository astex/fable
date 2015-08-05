from datetime import datetime
from dateutil.parser import parse
from sqlalchemy.ext.declarative import declared_attr
from app.lib.database import db


class ModelMixin(object):
    """A base mixin for all models."""

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __str__(self):
        return '<{} (id={})>'.format(self.__class__.__name__, self.id_)

    def __repr__(self):
        return str(self)

    id = db.Column(db.Integer, primary_key=True)

    def get_dictionary(self):
        d = {}
        for column in self.__table__.columns:
            key = column.key
            value = getattr(self, column.key)

            if isinstance(value, datetime):
                value = value.isoformat()

            d[key] = value
        return d
