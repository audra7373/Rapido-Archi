from app import models
from flask import Flask
from .database import init_db
from app.routes.Department_routes import department_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(department_bp)
    init_db()
    
    
    return app