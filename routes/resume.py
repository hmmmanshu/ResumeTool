from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db

resume_bp = Blueprint('resume', __name__)

@resume_bp.route('/create_from_scratch', methods=['POST'])
@jwt_required()
def create_resume_from_scratch():
    pass

@resume_bp.route('/create_from_code', methods=['POST'])
@jwt_required()
def create_resume_from_code():
    pass

@resume_bp.route('/create_from_resume', methods=['POST'])
@jwt_required()
def create_resume_from_resume():
    pass