import os


def config_app(app):
    db_uri = os.environ.get('DB_URI')

    app.config['JWT_SECRET_KEY'] = 'frase-secreta'
    app.config['DEBUG'] = True
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
