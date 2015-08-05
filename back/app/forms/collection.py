import wtforms as wtf
from app.forms.base import Form
from app.forms import validators
from app.models.collection import Collection, Story, Target


class CollectionForm(Form):
    name = wtf.TextField(validators=[wtf.validators.Length(max=20)])
    blurb = wtf.TextField(validators=[wtf.validators.Length(max=255)])
    description = wtf.TextField()


class StoryForm(Form):
    collection_id = wtf.IntegerField(validators=[
        validators.ForeignKey(Collection, 'id'),
        validators.Constant(Story, 'collection_id')
    ])
    description = wtf.TextField()


class TargetForm(Form):
    story_id = wtf.IntegerField(validators=[
        validators.ForeignKey(Story, 'id'),
        validators.Constant(Target, 'story_id')
    ])
    description = wtf.TextField()
