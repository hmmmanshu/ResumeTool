from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import OpenAIThread
from services.openai_services import generate_cover_letter, create_thread
from utils.wipe_utils import wipe_user_session

generate_bp = Blueprint("generate", __name__)


@generate_bp.route("/cover_letter", methods=["POST"])
@jwt_required()
def generate_cover_letter():
    # Initial call from dashboard to this function
    user_id = get_jwt_identity()
    data = request.form
    thread_id = OpenAIThread.query.filter_by(user_id=user_id).first().id

    if "file" in request.files:
        cover_letter = generate_cover_letter(
            f"Generate a short {data['tone']} cover letter for the following job description:\n\n{data['job_description']} based on the file attached as resume.",
            thread_id,
            request.files["file"],
            user_id,
        )
    else:
        cover_letter = generate_cover_letter(
            f"Generate a short {data['tone']} cover letter for the following job description:\n\n{data['job_description']}.",
            thread_id,
        )
    return jsonify({"generated_text": cover_letter}), 200


@generate_bp.route("/cover_letter_modify", methods=["POST"])
@jwt_required()
def modify_cover_letter():
    # Imrpove the cover letter generated in above step
    # The prompt passed to generate_text() might need improvement. This is being fed from user directly
    user_id = get_jwt_identity()
    data = request.form
    thread_id = OpenAIThread.query.filter_by(id=user_id).first().thread_id
    cover_letter = generate_cover_letter(data["job_description"], thread_id)


@generate_bp.route("/start_over", methods=["GET"])
@jwt_required()
def start_over():
    user_id = get_jwt_identity()
    wipe_user_session(user_id)
    create_thread(user_id)
    return jsonify({"message": "Thread created."}), 200
