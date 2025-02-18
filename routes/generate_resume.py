from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import OpenAIThread
from services.openai import generate_text, create_thread
from utils.wipe_utils import wipe_user_session
from utils.resume_utils import generate_pdf_from_latex
import config

resume_bp = Blueprint("resume", __name__)

# We could clear the thread here
@resume_bp.route("/resume_from_text", methods=["POST"])
@jwt_required()
def generate_resume_from_text():
    print("Generate resume called")
    user_id = get_jwt_identity()
    data = request.form
    # Modify the user thread to use the other assistant
    thread_id = OpenAIThread.query.filter_by(user_id=user_id).first().id

    resume = generate_text(
        f"Generate a latex resume the following job description:\n\n{data['job_description']}.",
        thread_id,
        config.Config.OPENAI_ASSISTANT_RESUME_CREATE,
    )
    pdf_file = generate_pdf_from_latex(resume)
    return send_file(pdf_file, mimetype="application/pdf", as_attachment=False)

@resume_bp.route("/resume_from_text_modify", methods=["POST"])
@jwt_required()
def modify_text_resume_code():
    print("Modify resume called")
    user_id = get_jwt_identity()
    data = request.form
    # Modify the user thread to use the other assistant
    thread_id = OpenAIThread.query.filter_by(user_id=user_id).first().id

    resume = generate_text(
        data['job_description'],
        thread_id,
        config.Config.OPENAI_ASSISTANT_RESUME_CREATE,
    )
    pdf_file = generate_pdf_from_latex(resume)
    return send_file(pdf_file, mimetype="application/pdf", as_attachment=False)
    

@resume_bp.route("/start_over", methods=["GET"])
@jwt_required()
def start_over():
    user_id = get_jwt_identity()
    wipe_user_session(user_id)
    create_thread(user_id)
    return jsonify({"message": "Thread created."}), 200
