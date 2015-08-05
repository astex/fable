import wtforms as wtf

from app.models.user import User
from app.models.deployment import Deployment
from app.models.collection import Collection, Story, Target
from app.models.run import Run, Step, Result, Action

from app.forms.base import Form
from app.forms import validators


class RunForm(Form):
    collection_id = wtf.IntegerField(validators=[
        validators.ForeignKey(Collection, 'id'),
        validators.Constant(Run, 'collection_id'),
        wtf.validators.Required()
    ])
    user_id = wtf.IntegerField(validators=[
        validators.ForeignKey(User, 'id'),
        validators.Constant(Run, 'user_id'),
        wtf.validators.Required()
    ])
    deployment_id = wtf.IntegerField(validators=[
        validators.ForeignKey(Deployment, 'id'),
        validators.Constant(Run, 'deployment_id'),
        wtf.validators.Required()
    ])

    finished = wtf.DateTimeField()
    status = wtf.TextField(validators=[
        validators.Enum(['incomplete', 'success', 'failure', 'resolved'])
    ])


class StepForm(Form):
    run_id = wtf.IntegerField(validators=[
        validators.ForeignKey(Run, 'id'),
        validators.Constant(Step, 'run_id'),
        wtf.validators.Required()
    ])
    story_id = wtf.IntegerField(validators=[
        validators.ForeignKey(Story, 'id'),
        validators.Constant(Step, 'story_id'),
        wtf.validators.Required()
    ])

    finished = wtf.DateTimeField()
    status = wtf.TextField(validators=[
        validators.Enum(['incomplete', 'success', 'failure', 'resolved'])
    ])


class ResultForm(Form):
    step_id = wtf.IntegerField(validators=[
        validators.ForeignKey(Step, 'id'),
        validators.Constant(Result, 'step_id'),
        wtf.validators.Required()
    ])
    target_id = wtf.IntegerField(validators=[
        validators.ForeignKey(Target, 'id'),
        validators.Constant(Result, 'target_id'),
        wtf.validators.Required()
    ])

    status = wtf.TextField(validators=[
        validators.Enum(['success', 'failure', 'resolved'])
    ])


class ActionForm(Form):
    result_id = wtf.IntegerField(validators=[
        validators.ForeignKey(Result, 'id'),
        validators.Constant(Action, 'result_id'),
        wtf.validators.Required()
    ])
    user_id = wtf.IntegerField(validators=[
        validators.ForeignKey(User, 'id'),
        validators.Constant(Action, 'user_id'),
        wtf.validators.Required()
    ])
    type = wtf.TextField(validators=[
        validators.Enum(['commented', 'resolved']),
        wtf.validators.Required()
    ])
    description = wtf.TextField()
