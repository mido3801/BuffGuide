import os

from flask import Flask
from flask_login import LoginManager
from app.user import User
from oauthlib.oauth2 import WebApplicationClient


# Function to create Flask app object.
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'buffguide.sqlite'),
        GOOGLEMAPS_KEY="temp"
    )

    # For testing purposes.
    if test_config is None:
        # load the instance config, if it exists when it testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import parse
    parse.init_app(app)

    from . import map
    app.register_blueprint(map.bp)
    app.add_url_rule('/', endpoint='index')



    return app
