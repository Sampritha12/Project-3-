from flask import Blueprint, jsonify
from app import db, es
from app.models import PracticeSpecialization  # Ensure this model exists

practice_specialization_bp = Blueprint("practice_specialization", __name__)

@practice_specialization_bp.route('/sync', methods=['POST'])
def sync_practice_specialization():
    practice_specializations = PracticeSpecialization.query.all()
    for prac_spec in practice_specializations:
        es.index(index="practice_specialization_index", id=prac_spec.id, document={
            "practice_id": prac_spec.practice_id,
            "specialization_id": prac_spec.specialization_id
        })
    return jsonify({"message": "Practice Specialization data synced successfully!"})
