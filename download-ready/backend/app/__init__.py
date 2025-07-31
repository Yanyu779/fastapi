from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    CORS(app)
    
    from app.routes import api
    app.register_blueprint(api, url_prefix='/api')
    
    with app.app_context():
        db.create_all()
    
    return app