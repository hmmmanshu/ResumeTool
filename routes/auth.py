from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from services.openai import create_thread
from utils.wipe_utils import wipe_user_session

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    hashed_pw = generate_password_hash(data["password"])
    new_user = User(name=data["name"], email=data["email"], password_hash=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()
    if user and check_password_hash(user.password_hash, data["password"]):
        print("User is valid, generating access token")
        access_token = create_access_token(identity=str(user.id))
        create_thread(user.id)
        return jsonify(access_token=access_token)
    return jsonify({"message": "Invalid credentials"}), 401


@auth_bp.route("/logout", methods=["GET"])
@jwt_required()
def logout():
    user_id = get_jwt_identity()
    wipe_user_session(user_id)
    return jsonify({"message": "User logged out"}), 200
