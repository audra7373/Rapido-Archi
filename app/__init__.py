from app import models
from flask import Flask
from .database import init_db
from app.routes.Department_routes import department_bp
from app.routes.upload_routes import upload_bp
from app.routes.rule_routes import rule_bp
from app.routes.web_routes import web_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(department_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(rule_bp)
    app.register_blueprint(web_bp)
    init_db()
    
    return app