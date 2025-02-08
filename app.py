from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from models import db
from routes.auth import auth_bp
from routes.generate import generate_bp
from routes.health import health_bp
from flask_cors import CORS

import config

app = Flask(__name__)
CORS(app)
app.config.from_object(config.Config)

db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(health_bp, url_prefix="/api/health")
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(generate_bp, url_prefix="/api/generate")
