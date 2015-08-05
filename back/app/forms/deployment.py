import wtforms as wtf
from wtforms.ext.dateutil.fields import DateTimeField
from app.forms.base import Form
from app.forms import validators


class DeploymentForm(Form):
    target = DateTimeField()
