from app.views.base import AdminChangeRestView
from app.controllers.deployment import DeploymentController


class DeploymentView(AdminChangeRestView):
    def get_controller(self):
        return DeploymentController()
