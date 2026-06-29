import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restx import Api
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from app.utils.datetime_utils import PeruJSONProvider

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
api = Api(
    title='API Iluminación Inteligente',
    version='1.0',
    description='API REST para monitoreo y control de iluminación inteligente',
    doc='/docs'
)


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('app.config.config.Config')

    if test_config is not None:
        app.config.update(test_config)

    app.json_provider_class = PeruJSONProvider
    app.json = app.json_provider_class(app)

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from app.routes import register_routes
    register_routes(api)
    api.init_app(app)

    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)

    if not app.config.get('TESTING', False):
        with app.app_context():
            from app import models
            db.create_all()

    return app
