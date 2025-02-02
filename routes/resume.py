from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Resume
from services.s3_upload import upload_file_to_s3

resume_bp = Blueprint('resume', __name__)

@resume_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_resume():
    user_id = get_jwt_identity()
    print(request.files)
    file = request.files['file']
    if not file:
        return jsonify({"error": "No file provided"}), 400

    file_url = upload_file_to_s3(file)
    new_resume = Resume(user_id=user_id, file_url=file_url)
    db.session.add(new_resume)
    db.session.commit()

    return jsonify({"message": "Resume uploaded", "file_url": file_url})

@resume_bp.route('/list', methods=['GET'])
@jwt_required()
def list_resumes():
    user_id = get_jwt_identity()
    resumes = Resume.query.filter_by(user_id=user_id).all()
    return jsonify([{"resume_id": r.id, "file_url": r.file_url} for r in resumes])


# TODO: Add fucntionality to delete or download resume