import importlib
import os

from flasgger import Swagger
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from models.db import db
from config import config_app

# ToDo: remove this
# Just to create the models in the DB
from models.task import Task  # noqa
from models.user import User  # noqa


def create_app(env) -> Flask:
    app = Flask(__name__)
    CORS(app)
    import_blueprints(app)
    Swagger(app)
    config_app(app, env)
    app_context = app.app_context()
    app_context.push()
    db.init_app(app)
    db.create_all()
    CORS(app)
    JWTManager(app)
    db.init_app(app)
    return app


def import_blueprints(app):
    routes_path = os.listdir(os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') + '/routes')
    for file in routes_path:
        if file.endswith('route.py'):
            module_name = file[:-3]
            module = importlib.import_module('routes.' + module_name)
            app.register_blueprint(module.blueprint)


app = create_app(os.getenv('FLASK_ENV', 'dev'))
