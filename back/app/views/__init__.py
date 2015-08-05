from app.views import user, deployment, collection, run


def register(app):
    user.UserView.register(app)
    user.SessionView.register(app)

    deployment.DeploymentView.register(app)

    collection.CollectionView.register(app)
    collection.StoryView.register(app)
    collection.TargetView.register(app)

    run.RunView.register(app)
    run.StepView.register(app)
    run.ResultView.register(app)
    run.ActionView.register(app)
