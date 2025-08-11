from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    get_jwt_identity, get_jwt
)
from models import UserModel
from db import db
from schemas import UserSchema

# Blacklist en memoria (en producción usar Redis o DB)
BLOCKLIST = set()

blp = Blueprint("users", __name__, description="Operations on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="Username already exists.")

        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return user


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200

        abort(401, message="Invalid credentials.")


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user_id, fresh=False)
        return {"access_token": new_access_token}, 200


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]  # ID único del token
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out."}, 200


@blp.route("/logout_refresh")
class UserLogoutRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Refresh token successfully logged out."}, 200


@blp.route("/protected")
class ProtectedResource(MethodView):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        return {"message": f"Hello user {current_user_id}, you have access!"}, 200
