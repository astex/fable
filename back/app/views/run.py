from flask import request
from app.views.base import RestView
from app.controllers.run import (
    RunController, StepController, ResultController, ActionController
)
from app.permissions.user import login_need, admin_need
from app.permissions.run import RunOwnerNeed, StepOwnerNeed


class RunView(RestView):
    def get_controller(self):
        return RunController()

    @login_need
    def index(self):
        return super(RunView, self).index()

    @login_need
    def get(self, id_):
        return super(RunView, self).get(id_)

    @login_need
    def post(self):
        return super(RunView, self).post()

    def put(self, id_):
        with admin_need | RunOwnerNeed(id_):
            return super(RunView, self).put(id_)

    def delete(self, id_):
        with admin_need | RunOwnerNeed(id_):
            return super(RunView, self).put(id_)


class StepView(RestView):
    def get_controller(self):
        return StepController()

    @login_need
    def index(self):
        return super(StepView, self).index()

    @login_need
    def get(self, id_):
        return super(StepView, self).get(id_)

    def get_change_need(self):
        return admin_need | RunOwnerNeed(request.json.get('run_id'))

    def post(self):
        with self.get_change_need():
            return super(StepView, self).post()

    def put(self, id_):
        with self.get_change_need():
            return super(StepView, self).put(id_)

    def delete(self, id_):
        with self.get_change_need():
            return super(StepView, self).delete(id_)


class ResultView(RestView):
    def get_controller(self):
        return ResultController()

    @login_need
    def index(self):
        return super(ResultView, self).index()

    @login_need
    def get(self, id_):
        return super(ResultView, self).get(id_)

    def get_change_need(self):
        return admin_need | StepOwnerNeed(request.json.get('step_id'))

    def post(self):
        with self.get_change_need():
            return super(StepView, self).post()

    def put(self, id_):
        with self.get_change_need():
            return super(StepView, self).put(id_)

    def delete(self, id_):
        with self.get_change_need():
            return super(StepView, self).delete(id_)


class ActionView(RestView):
    def get_controller(self):
        return ActionController()

    @login_need
    def index(self):
        return super(ActionView, self).index()

    @login_need
    def get(self, id_):
        return super(ActionView, self).get(id_)

    @login_need
    def post(self):
        return super(ActionView, self).post()
