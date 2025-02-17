from sqlite3 import Cursor
from flask import Blueprint, request, jsonify, render_template
from app.models import Doctor, Practice,DoctorSpecialization,Specialization,PracticeSpecialization, DoctorPractice,db
from app.services.elasticsearch_service import DOCTOR_PRACTICE_INDEX, DOCTOR_SPECIALIZATION_INDEX, PRACTICE_SPECIALIZATION_INDEX, SPECIALIZATION_INDEX, es


search_bp = Blueprint('search_bp', __name__)

@search_bp.route('/search', methods=['GET'])
def search():
    from app import app
    query = request.args.get('q', '')

    if not query:
        return jsonify({"error": "Missing query parameter"}), 400

    specialization_results = es.search(index="specialization_index", body={
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["name", "description"]
            }
        }
    })

    doctor_specialization_results = es.search(index="doctor_specialization_index", body={
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["doctor.name", "specialization.name"]
            }
        }
    })

    practice_specialization_results = es.search(index="practice_specialization_index", body={
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["practice.name", "specialization.name"]
            }
        }
    })

    return jsonify({
        "specializations": specialization_results['hits']['hits'],
        "doctor_specializations": doctor_specialization_results['hits']['hits'],
        "practice_specializations": practice_specialization_results['hits']['hits']
    })



