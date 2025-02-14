from flask import Blueprint, request, jsonify, render_template
from app.models import Doctor, Practice, db
from app.services.elasticsearch_service import (
    search_doctors_in_es,
    search_practices_in_es,
    search_doctor_by_id_in_es,
    search_practice_by_id_in_es
)

search_bp = Blueprint('search_bp', __name__)

@search_bp.route('/search/doctors', methods=['GET'])
def search_doctors():
    name = request.args.get('name')
    specialization = request.args.get('specialization')
    doctors = search_doctors_in_es(name=name, specialization=specialization)
    return jsonify(doctors)

@search_bp.route('/search/practices', methods=['GET'])
def search_practices():
    name = request.args.get('name')
    specialization = request.args.get('specialization')
    practices = search_practices_in_es(name=name, specialization=specialization)
    return jsonify(practices)

