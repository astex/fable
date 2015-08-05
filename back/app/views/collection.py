from app.views.base import AdminChangeRestView
from app.controllers.collection import (
    CollectionController, StoryController, TargetController
)


class CollectionView(AdminChangeRestView):
    def get_controller(self):
        return CollectionController()


class StoryView(AdminChangeRestView):
    def get_controller(self):
        return StoryController()


class TargetView(AdminChangeRestView):
    def get_controller(self):
        return TargetController()
