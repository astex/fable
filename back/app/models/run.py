from sqlalchemy.sql import func

from app.lib.database import db
from app.models import ModelMixin


class Run(ModelMixin, db.Model):
    collection_id = db.Column(
        db.Integer, db.ForeignKey('collection.id'),
        nullable=False
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'),
        nullable=False
    )
    deployment_id = db.Column(
        db.Integer, db.ForeignKey('deployment.id'),
        nullable=False
    )

    started = db.Column(db.DateTime, default=func.now())
    finished = db.column(db.DateTime)

    status = db.Column(
        db.Enum('incomplete', 'success', 'failure', 'resolved'),
        nullable=False, default='incomplete', index=True
    )


class Step(ModelMixin, db.Model):
    run_id = db.Column(
        db.Integer, db.ForeignKey('run.id'),
        nullable=False
    )
    story_id = db.Column(
        db.Integer, db.ForeignKey('story.id'),
        nullable=False
    )

    started = db.Column(db.DateTime, default=func.now())
    finished = db.Column(db.DateTime)

    status = db.Column(
        db.Enum('incomplete', 'success', 'failure', 'resolved'),
        nullable=False, default='incomplete', index=True
    )


class Result(ModelMixin, db.Model):
    step_id = db.Column(
        db.Integer, db.ForeignKey('step.id'),
        nullable=False
    )
    target_id = db.Column(
        db.Integer, db.ForeignKey('target.id'),
        nullable=False
    )

    created = db.Column(db.DateTime, default=func.now())

    status = db.Column(
        db.Enum('success', 'failure', 'resolved'),
        nullable=False, default='incomplete', index=True
    )


class Action(ModelMixin, db.Model):
    result_id = db.Column(
        db.Integer, db.ForeignKey('result.id'),
        nullable=False
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'),
        nullable=False
    )

    created = db.Column(db.DateTime, default=func.now())

    type = db.Column(
        db.Enum('commented', 'resolved'),
        nullable=False, default='commented'
    )
    description = db.Column(db.UnicodeText)
