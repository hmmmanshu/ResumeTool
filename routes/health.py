from flask import Blueprint, jsonify
from models import Health, db
from sqlalchemy.exc import SQLAlchemyError

health_bp = Blueprint("health", __name__)


@health_bp.route("/", methods=["GET"])
def health():
    try:
        health_record = Health.query.filter_by(status="healthy").first()

        if not health_record:
            health_record = Health(status="healthy")
            db.session.add(health_record)
            db.session.commit()

        health_status = health_record.status
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return jsonify({"error": "Database operation failed"}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

    return jsonify({"status": health_status}), 200
