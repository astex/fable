from app.controllers.base import RestController
from app.models.run import Run, Step, Result, Action
from app.forms.run import RunForm, StepForm, ResultForm, ActionForm


class RunController(RestController):
    Model = Run
    filters = {
        'deployment_id': lambda d: Run.deployment_id == d.get('deployment_id')
    }

    def get_form(self, filter_data):
        return RunForm


class StepController(RestController):
    Model = Step
    filters = {
        'deployment_id': lambda d: Run.deployment_id == d.get('deployment_id')
    }

    def query(self, filter_data):
        q = super(StepController, self).query(filter_data)
        if 'deployment_id' in filter_data:
            q = q.join(Run)
        return q

    def get_form(self, filter_data):
        return StepForm


class ResultController(RestController):
    Model = Result
    filters = {
        'deployment_id': lambda d: Run.deployment_id == d.get('deployment_id')
    }

    def query(self, filter_data):
        q = super(ResultController, self).query(filter_data)
        if 'deployment_id' in filter_data:
            q = q.join(Step).join(Run)
        return q

    def get_form(self, filter_data):
        return ResultForm


class ActionController(RestController):
    Model = Action
    filters = {
        'deployment_id': lambda d: Run.deployment_id == d.get('deployment_id')
    }

    def query(self, filter_data):
        q = super(ActionController, self).query(filter_data)
        if 'deployment_id' in filter_data:
            q = q.join(Result).join(Step).join(Run)
        return q

    def get_form(self, filter_data):
        return ActionForm
