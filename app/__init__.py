from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import Config
from elasticsearch import Elasticsearch


db = SQLAlchemy()
migrate = Migrate()
es = Elasticsearch(["http://localhost:9200"])

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})  
    app.config.from_object(Config)  

    db.init_app(app)  
    migrate.init_app(app, db)  
   

   
    from app.controllers.doctor_controller import doctor_bp
    from app.controllers.practice_controller import practice_bp
    from app.controllers.search_controller import search_bp
    from app.controllers.specialization_controller import specialization_bp
    from app.controllers.doctor_practice_controller import doctor_practice_bp  
    from app.controllers.doctor_specialization_controller import doctor_specialization_bp
    from app.controllers.practice_specialization_controller import practice_specialization_bp  



   
    app.register_blueprint(doctor_bp, url_prefix='/doctors')
    app.register_blueprint(practice_bp, url_prefix='/practices')
    app.register_blueprint(search_bp, url_prefix='/search')
    app.register_blueprint(specialization_bp, url_prefix="/specialization")
    app.register_blueprint(doctor_practice_bp, url_prefix='/doctor_practice')
    app.register_blueprint(doctor_specialization_bp, url_prefix='/doctor_specialization')
    app.register_blueprint(practice_specialization_bp, url_prefix='/practice_specialization')


    app.es = es

    return app
