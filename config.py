import os


def config_app(app, env_name):
    test_db_uri = os.environ.get('TEST_DB_URI')
    db_uri = os.environ.get('DB_URI')

    app.config['JWT_SECRET_KEY'] = 'frase-secreta'
    app.config['DEBUG'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['SWAGGER'] = {
        'title': 'Flask API Starter Kit',
    }

    if env_name == 'dev':
        print("Running in development mode.")
        app.config['DEBUG'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = test_db_uri or 'sqlite:///db.sqlite'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    elif env_name == 'test':
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = test_db_uri or 'sqlite:///db.sqlite'
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    elif env_name == 'prod':
        print("Running in production mode.")
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    return app
