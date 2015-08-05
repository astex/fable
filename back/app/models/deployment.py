from app.lib.database import db
from app.models import ModelMixin


class Deployment(ModelMixin, db.Model):
    target = db.Column(db.DateTime, nullable=False)
