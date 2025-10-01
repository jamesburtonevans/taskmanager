import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS

def create_app(test_config=None):
    app = Flask(
        __name__, 
        instance_relative_config=True,
        static_folder='../frontend/dist', 
        static_url_path='/'
    )
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register your API blueprint
    from .api_routes import routes as api_routes
    app.register_blueprint(api_routes.bp) 

    CORS(app)

    from . import db
    db.init_app(app)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_vue_app(path):
        return send_from_directory(app.static_folder, 'index.html')

    return app