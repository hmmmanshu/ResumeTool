from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.openai_services import create_thread, generate_resume_code

resume_bp = Blueprint("resume", __name__)


@resume_bp.route("/create_from_text", methods=["POST"])
@jwt_required()
def create_resume_from_scratch():
    user_id = get_jwt_identity()
    data = request.form
    thread_id = create_thread(user_id)
    user_text = data["user_text"]

    latex_code = generate_resume_code(user_text, thread_id)
    return latex_code


@resume_bp.route("/enhance_resume", methods=["POST"])
@jwt_required()
def enhance_resume():
    pass


@resume_bp.route("/create_from_code", methods=["POST"])
@jwt_required()
def create_resume_from_code():
    pass


@resume_bp.route("/create_from_resume", methods=["POST"])
@jwt_required()
def create_resume_from_resume():
    pass
