import os
import secrets
from datetime import timedelta
from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from resources.store import blp as StoreBlueprint
from resources.item import blp as ItemBlueprint
from resources.tags import blp as TagsBlueprint
from resources.user import blp as UserBlueprint
from resources.user import BLOCKLIST

from db import db
import models


def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Store and Item API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # JWT Config
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", secrets.token_hex(32))
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)   # Access token expira en 15 minutos
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)     # Refresh token expira en 30 días

    db.init_app(app)
    api = Api(app)

    # Inicializar JWT
    jwt = JWTManager(app)

    # Callbacks opcionales para personalizar errores de JWT
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {"message": "The token has expired.", "error": "token_expired"}, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {"message": "Signature verification failed.", "error": "invalid_token"}, 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {"message": "Request does not contain an access token.", "error": "authorization_required"}, 401

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    # Registrar blueprints
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(TagsBlueprint)
    api.register_blueprint(UserBlueprint)

    with app.app_context():
        db.create_all()
        print("Tablas creadas o ya existen")

    return app
