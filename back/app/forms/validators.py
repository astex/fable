import wtforms as wtf
from app.lib.database import db


class Unique(object):
    def __init__(self, Model, name):
        self.Model = Model
        self.name = name

        self.message = 'There is already a record with that {}.'.format(name)

    def __call__(self, form, field):
        u = (db.session.query(self.Model)
            .filter(getattr(self.Model, self.name) == field.data))
        if form.id.data:
            u = u.filter(self.Model.id != form.id.data)

        if u.first():
            raise wtf.ValidationError(self.message)


class Password(object):
    def __init__(self, Model, id_field):
        self.Model = Model
        self.id_field = id_field

    def __call__(self, form, field):
        u = (db.session.query(self.Model)
            .filter(
                getattr(self.Model, self.id_field) == \
                    getattr(form, self.id_field).data
            )
            .first())

        if not u:
            return

        if not u.check_password(field.data):
            raise wtf.ValidationError('The password and email do not match.')


class ForeignKey(object):
    def __init__(self, Model, name):
        self.Model = Model
        self.name = name

    def __call__(self, form, field):
        m = (db.session.query(self.Model)
            .filter(getattr(self.Model, self.name) == field.data)
            .first())
        if not m:
            raise wtf.ValidationError('There is no {} with that {}.'.format(
                self.Model.__name__.lower(), self.name
            ))


class Constant(object):
    def __init__(self, Model, name):
        self.Model = Model
        self.name = name

    def __call__(self, form, field):
        if form.id.data:
            m = (db.session.query(self.Model)
                .filter(self.Model.id == form.id.data)
                .first())
            if not getattr(m, self.name) == field.data:
                raise ValidationError('This field is constant.')


class Enum(object):
    def __init__(self, choices):
        self.choices = choices

    def __call__(self, form, field):
        if field.data and field.data not in self.choices:
            raise wtf.ValidationError('That is not a valid selection.')
