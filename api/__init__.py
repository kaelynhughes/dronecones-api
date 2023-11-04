import os
from flask import Flask
from . import db, auth, customer, manager, employee
from flask_cors import CORS


# the application factory! lets us start the app running
def create_app(test_config=None):
    # this whole function creates the app & configures some things
    # __name__ represents the current module
    # instance_relative_config tells the app whether to look for config files relative to the instance folder
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "api.sqlite"),
    )

    # this will load in our config file if we have one, or our test config if we're testing
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists, where we'll put our database
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # home route
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(customer.bp)
    app.register_blueprint(employee.bp)
    app.register_blueprint(manager.bp)

    return app
