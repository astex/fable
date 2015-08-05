from sqlalchemy import or_
from sqlalchemy.orm import aliased

from app.controllers.base import RestController
from app.models.user import User
from app.models.run import Run, Step, Result, Action
from app.forms.user import UserForm


ActionRun = aliased(Run, name='action_run')
class UserController(RestController):
    Model = User
    filters = {
        'deployment_id': lambda d: or_(
            Run.deployment_id == d.get('deployment_id'),
            ActionRun.deployment_id == d.get('deployment_id')
        )
    }

    def query(self, filter_data):
        q = super(UserController, self).query(filter_data)
        if 'deployment_id' in filter_data:
            q = (q
                .join(Run, Run.user_id == User.id)
                .join(Action, Action.user_id == User.id)
                .join(Result, Result.id == Action.result_id)
                .join(Step, Step.id == Result.step_id)
                .join(ActionRun, ActionRun.id == Step.run_id)
            )
        return q

    def get_form(self, filter_data):
        return UserForm
