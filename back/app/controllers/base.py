import six
from werkzeug.exceptions import NotFound, BadRequest
from werkzeug.datastructures import MultiDict
from app.lib.database import db, commit


class RestController(object):
    Model = None

    filters = {}

    def query(self, filter_data):
        return db.session.query(self.Model)

    def filter(self, q, filter_data):
        for k, f in six.iteritems(self.filters):
            if k in filter_data:
                q = q.filter(f(filter_data))
        return q

    def get_form(self, filter_data):
        pass

    def index(self, filter_data):
        q = self.query(filter_data)
        q = self.filter(q, filter_data)
        return q.all()

    def get(self, id_, filter_data=None):
        if filter_data == None:
            filter_data = {}

        model = db.session.query(self.Model).filter(self.Model.id==id_).first()
        if not model:
            raise NotFound
        return model

    def post(self, data, filter_data):
        model = self.Model()
        form = self.get_form(filter_data)(formdata=MultiDict(data))

        if not form.validate():
            raise BadRequest(form.errors)

        form.populate_obj(model)
        db.session.add(model)
        commit()

        return model

    def put(self, id_, data, filter_data):
        model = self.get(id_)
        form = self.get_form(filter_data)(formdata=MultiDict(data))

        if not str(form.id.data) == str(id_):
            raise BadRequest(['The id in the model and the uri do not match.'])
        if not form.validate():
            raise BadRequest(form.errors.values())
        
        form.populate_obj(model)
        db.session.add(model)
        commit()
        return model

    def delete(self, id_, filter_data):
        model = self.get(id_)
        db.session.delete(model)
        commit()
        return {}
