from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load config from Config class

    db.init_app(app)  # Initialize db
    migrate.init_app(app, db)  # Initialize migrations
    CORS(app)  # Enable CORS

    # Import controllers (blueprints)
    from app.controllers.doctor_controller import doctor_bp
    from app.controllers.practice_controller import practice_bp
    from app.controllers.search_controller import search_bp

    # Register blueprints with URL prefixes
    app.register_blueprint(doctor_bp, url_prefix='/doctors')
    app.register_blueprint(practice_bp, url_prefix='/practices')
    app.register_blueprint(search_bp, url_prefix='/search')

    return app
