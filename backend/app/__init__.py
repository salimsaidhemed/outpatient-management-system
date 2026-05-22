from flask import Flask
from flask_cors import CORS

from .config import Config
from .extensions import db
from .routes import api


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})
    db.init_app(app)

    app.register_blueprint(api, url_prefix="/api")

    with app.app_context():
        db.create_all()

    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    return app
