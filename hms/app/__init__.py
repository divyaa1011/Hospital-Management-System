"""App factory - keep it simple."""

from flask import Flask, jsonify
from .config import Config
from .db import db
from .logger import configure_logging

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    configure_logging()

    # initialize database
    db.init_app(app)

    # register routes
    from .routes import api_blueprint
    app.register_blueprint(api_blueprint)

    # centralized error handler for any uncaught exception
    @app.errorhandler(Exception)
    def handle_all_exceptions(e):  # keep a simple fallback
        # avoid exposing internals
        app.logger.exception("Unhandled exception")
        return jsonify({"error": "internal server error"}), 500

    with app.app_context():
        db.create_all()

    return app
