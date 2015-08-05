from app.lib.database import db
from app.models import ModelMixin


class Collection(ModelMixin, db.Model):
    name = db.Column(db.Unicode(length=20))
    blurb = db.Column(db.Unicode(length=255))
    description = db.Column(db.UnicodeText)


class Story(db.Model, ModelMixin):
    collection_id = db.Column(
        db.Integer, db.ForeignKey('collection.id'),
        nullable=False
    )
    description = db.Column(db.UnicodeText)


class Target(db.Model, ModelMixin):
    story_id = db.Column(
        db.Integer, db.ForeignKey('story.id'),
        nullable=False
    )
    description = db.Column(db.UnicodeText)
