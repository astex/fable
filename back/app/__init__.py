from flask import Flask
from flask.ext.cors import CORS


def create_app(config):
    app = Flask(__name__)
    app.config.from_pyfile(config)

    CORS(
        app,
        origins=app.config['CORS_ORIGINS'],
        supports_credentials=True
    )

    from app.lib.database import db
    db.init_app(app)

    from app import views
    views.register(app)

    with app.app_context():
        db.create_all()

    from app.lib.session import SessionInterface
    app.session_interface = SessionInterface()

    from app.lib import exceptions
    exceptions.register(app)

    return app
