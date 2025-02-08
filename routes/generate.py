from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, OpenAIThread
from services.openai import generate_text

generate_bp = Blueprint('generate', __name__)

@generate_bp.route('/cover_letter', methods=['POST'])
@jwt_required()
def generate_cover_letter():
    user_id = get_jwt_identity()
    data = request.form
    print("User id in generate cover rout", user_id)
    thread_id = OpenAIThread.query.filter_by(user_id=user_id).first().id
    print(f"Inside /cover_letter, Thread recieved, {thread_id}")
    if 'file' in request.files:
        cover_letter = generate_text(
            f"Generate a short {data['tone']} cover letter for the following job description:\n\n{data['job_description']} based on the file attached as resume.", thread_id, request.files['file']
        )
    else:
        cover_letter = generate_text(
            f"Generate a short {data['tone']} cover letter for the following job description:\n\n{data['job_description']}.", thread_id
        )
    return jsonify({"generated_text": cover_letter}), 200

@generate_bp.route('/cover_letter_modify', methods=['POST'])
@jwt_required()
def modify_cover_letter():
    # Imrpove the cover letter generated in above step
    # The prompt passed to generate_text() might need improvement. This is being fed from user directly
    user_id = get_jwt_identity()
    data = request.form
    thread_id = Thread.query.filter_by(id=user_id).first().thread_id
    print(f"Inside /cover_letter_modfiy, Thread recieved, {thread_id}")
    cover_letter = generate_text(
        data['job_description'], thread_id
    )

@generate_bp.route('/analyze_resume', methods=['POST'])
@jwt_required()
def analyze_resume():
    # This function is incomplete. improve it to scan resume and suggest edits
    user_id = get_jwt_identity()
    data = request.get_json()

    enhanced_resume = generate_text(
        f"Improve the resume content with a {data['tone']} tone:\n\n{data['resume_id']}"
    )

    return jsonify({"enhanced_resume": enhanced_resume}), 200


@generate_bp.route('/enhance_resume', methods=['POST'])
@jwt_required
def enhance_resume():
    # Get the latex code for a resume and improve the resume
    return jsonify({"Not yet implemented"}), 200