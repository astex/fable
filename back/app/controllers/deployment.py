from app.controllers.base import RestController
from app.models.deployment import Deployment
from app.forms.deployment import DeploymentForm


class DeploymentController(RestController):
    Model = Deployment

    def get_form(self, filter_data):
        return DeploymentForm
