import wtforms as wtf
from app.forms import validators


class Form(wtf.Form):
    id = wtf.IntegerField()
