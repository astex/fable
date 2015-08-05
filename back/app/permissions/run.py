from flask import session
from app.lib.database import db
from app.models.run import Run, Step
from app.permissions.base import BaseNeed
from app.permissions.user import login_need


class RunOwnerNeed(BaseNeed):
    def __init__(self, run_id):
        self.run_id = run_id

    def is_met(self):
        return login_need and db.session.query(Run).filter(
            Run.id_ == self.run_id,
            Run.user_id == session.get('user_id')
        ).first()


class StepOwnerNeed(BaseNeed):
    def __init__(self, step_id):
        self.step_id = step_id

    def is_met(self):
        return login_need and db.session.query(Step).join(Run).filter(
            Step.id_ == self.step_id,
            Run.user_id == session.get('user_id')
        ).first()
