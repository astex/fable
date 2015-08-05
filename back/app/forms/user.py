import wtforms as wtf
from app.forms.base import Form
from app.forms import validators
from app.models.user import User


class UserForm(Form):
    name = wtf.TextField(validators=[wtf.validators.Length(max=30)])
    email = wtf.TextField(validators=[
        wtf.validators.Required(), wtf.validators.Email(),
        wtf.validators.Length(max=255),
        validators.Unique(User, 'email')
    ])
    password = wtf.TextField(validators=[
        wtf.validators.Required(), wtf.validators.Length(max=55)
    ])


class SessionForm(wtf.Form):
    email = wtf.TextField(validators=[
        wtf.validators.Length(max=30),
        validators.ForeignKey(User, 'email')
    ])
    password = wtf.TextField(validators=[
        wtf.validators.Required(), validators.Password(User, 'email')
    ])
