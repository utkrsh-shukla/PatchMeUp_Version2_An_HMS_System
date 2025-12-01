"""Flask application factory for HMS V2 API"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_cors import CORS
from flask_mail import Mail
from app.config import config


db = SQLAlchemy()
jwt = JWTManager()
cache = Cache()
mail = Mail()

def create_app(config_name=None):
    """Create and configure the Flask application"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
   
    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    mail.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    

    os.makedirs(os.path.join(app.root_path, '..', 'instance'), exist_ok=True)
    
    
    from app.api.auth import auth_bp
    from app.api.admin import admin_bp
    from app.api.doctor import doctor_bp
    from app.api.patient import patient_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(doctor_bp, url_prefix='/api/doctor')
    app.register_blueprint(patient_bp, url_prefix='/api/patient')
    
   
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'version': '2.0'}, 200
    
    return app
