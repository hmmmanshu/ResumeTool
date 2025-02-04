from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, GeneratedDocument, User
from services.ai_service import generate_text

generate_bp = Blueprint('generate', __name__)

@generate_bp.route('/cover_letter', methods=['POST'])
@jwt_required()
def generate_cover_letter():
    user_id = get_jwt_identity()
    data = request.form
    file = request.files['file']
    thread_id = User.query.filter_by(id=user_id).first().thread_id
    print(f"thread recieved, {thread_id}")
    cover_letter = generate_text(
        f"Generate a {data['tone']} cover letter for the following job description:\n\n{data['job_description']} based on the file attached as resume", thread_id, file
    )
    new_doc = GeneratedDocument(user_id=user_id, type="cover_letter", content=cover_letter, resume_id=data['resume_id'])
    db.session.add(new_doc)
    db.session.commit()

    return jsonify({"generated_text": cover_letter}), 200

@generate_bp.route('/analyze_resume', methods=['POST'])
@jwt_required()
def analyze_resume():
    # This function is incomplete. improve it to scan resume and suggest edits
    user_id = get_jwt_identity()
    data = request.get_json()

    enhanced_resume = generate_text(
        f"Improve the resume content with a {data['tone']} tone:\n\n{data['resume_id']}"
    )

    new_doc = GeneratedDocument(user_id=user_id, type="resume_enhancement", content=enhanced_resume)
    db.session.add(new_doc)
    db.session.commit()

    return jsonify({"enhanced_resume": enhanced_resume}), 200


@generate_bp.route('/enhance_resume', methods=['POST'])
@jwt_required
def enhance_resume():
    # Get the latex code for a resume and improve the resume
    return jsonify({"Not yet implemented"}), 200
    