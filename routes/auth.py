from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, OpenAIThread
from services.openai import create_thread

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_pw = generate_password_hash(data['password'])
    new_user = User(name=data['name'], email=data['email'], password_hash=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        print("User is valid, generating access token")
        access_token = create_access_token(identity=str(user.id))
        try:
            new_thread = OpenAIThread(id=create_thread(), user_id = user.id)
            db.session.add(new_thread)
            db.session.commit()
        except Exception as error:            
            print(error)
            return jsonify({"message": "OpenAI thread not created, please login again."}), 401
        return jsonify(access_token=access_token)
    return jsonify({"message": "Invalid credentials"}), 401

@auth_bp.route('/logout', methods=['GET'])
def logout():
    # Right now, the thread is not being delted from the assistant, but only the db. fix it
    # delete the thread_id of user from db
    # delete the files uploaded by user

    pass
    return jsonify({"message": "Called logout api"}), 201