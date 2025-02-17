from flask import Blueprint, jsonify
from app import db, es
from app.models import DoctorSpecialization  

doctor_specialization_bp = Blueprint("doctor_specialization", __name__)

@doctor_specialization_bp.route('/sync', methods=['POST'])
def sync_doctor_specialization():
    doctor_specializations = DoctorSpecialization.query.all()
    for doc_spec in doctor_specializations:
        es.index(index="doctor_specialization_index", id=doc_spec.id, document={
            "doctor_id": doc_spec.doctor_id,
            "specialization_id": doc_spec.specialization_id
        })
    return jsonify({"message": "Doctor Specialization data synced successfully!"})
