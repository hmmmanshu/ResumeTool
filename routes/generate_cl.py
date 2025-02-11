from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import OpenAIThread
import config
from services.openai import generate_text, create_thread
from utils.wipe_utils import wipe_user_session

generate_bp = Blueprint("generate", __name__)


@generate_bp.route("/cover_letter", methods=["POST"])
@jwt_required()
def generate_cover_letter():
    print("Generate cover letter called")
    user_id = get_jwt_identity()
    data = request.form
    thread_id = OpenAIThread.query.filter_by(user_id=user_id).first().id

    if "file" in request.files:
        cover_letter = generate_text(
            f"Generate a short {data['tone']} cover letter for the following job description:\n\n{data['job_description']} based on the file attached as resume.",
            thread_id,
            config.Config.OPENAI_ASSISTANT_COVER_LETTER_CREATE,
            request.files["file"],
            user_id,
        )
    else:
        cover_letter = generate_text(
            f"Generate a short {data['tone']} cover letter for the following job description:\n\n{data['job_description']}.",
            thread_id,
            config.Config.OPENAI_ASSISTANT_COVER_LETTER_CREATE
        )
    print(cover_letter)
    return jsonify({"generated_text": cover_letter}), 200


@generate_bp.route("/cover_letter_modify", methods=["POST"])
@jwt_required()
def modify_cover_letter():
    print("Enhance cover letter called")
    user_id = get_jwt_identity()
    print("user_id", user_id)
    data = request.form
    thread_id = OpenAIThread.query.filter_by(user_id=user_id).first().id
    cover_letter = generate_text(data["job_description"], thread_id, config.Config.OPENAI_ASSISTANT_COVER_LETTER_CREATE)
    print(cover_letter)
    return jsonify({"generated_text": cover_letter}), 200


@generate_bp.route("/start_over", methods=["GET"])
@jwt_required()
def start_over():
    user_id = get_jwt_identity()
    wipe_user_session(user_id)
    create_thread(user_id)
    return jsonify({"message": "Thread created."}), 200
