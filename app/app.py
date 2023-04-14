import importlib
import os

from flasgger import Swagger
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from prometheus_flask_exporter import PrometheusMetrics

from config import config_app
from models.db import db
from models.db import engine
# ToDo: remove this
# Just to create the models in the DB
from models.user import User  # noqa
from models.task import Task  # noqa


def import_blueprints(flask_app):
    routes_path = os.listdir(os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') + '/routes')
    for file in routes_path:
        if file.endswith('route.py'):
            module_name = file[:-3]
            module = importlib.import_module('routes.' + module_name)
            flask_app.register_blueprint(module.blueprint)


app = Flask(__name__)
PrometheusMetrics(app)
CORS(app)
import_blueprints(app)
Swagger(app)
config_app(app)
app_context = app.app_context()
app_context.push()
# db.init_app(app)
db.metadata.create_all(engine)
CORS(app)
JWTManager(app)
# db.init_app(app)
