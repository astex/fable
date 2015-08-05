from werkzeug.exceptions import default_exceptions
from flask import jsonify


def register(app):
    def jsonify_error(e):
        return jsonify(dict(status=e.code, short=e.name, data=e.description)), e.code

    for code in default_exceptions.keys():
        app.error_handler_spec[None][code] = jsonify_error
