from flask import Blueprint, jsonify
from app import db, es
from app.models import DoctorPractice  

doctor_practice_bp = Blueprint("doctor_practice", __name__)

@doctor_practice_bp.route('/sync', methods=['POST'])
def sync_doctor_practice():
    doctor_practices = DoctorPractice.query.all()
    for doc_prac in doctor_practices:
        es.index(index="doctor_practice_index", id=doc_prac.id, document={
            "doctor_id": doc_prac.doctor_id,
            "practice_id": doc_prac.practice_id
        })
    return jsonify({"message": "Doctor Practice data synced successfully!"})


@doctor_practice_bp.route("/doctors/<practice_id>", methods=["POST"])
def get_doctors_by_practice(practice_id):
    practice_query = {
        "query": {
            "term": { "practice_id": practice_id }
        }
    }
    
    practice_response = es.search(index="doctor_practice_index", body=practice_query)

    if practice_response["hits"]["total"]["value"] == 0:
        return jsonify({"message": "No doctors available for this practice."})

    doctor_ids = [hit["_source"]["doctor_id"] for hit in practice_response["hits"]["hits"]]

    doctor_query = {
        "query": {
            "terms": { "doctor_id": doctor_ids }
        }
    }

    doctor_response = es.search(index="doctors", body=doctor_query)

    doctors = [doc["_source"] for doc in doctor_response["hits"]["hits"]]

    return jsonify(doctors)

