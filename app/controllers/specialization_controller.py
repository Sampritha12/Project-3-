

from flask import Blueprint, jsonify
from app import es
from app.services.elasticsearch_service import SPECIALIZATION_INDEX
from app.models import Specialization

specialization_bp = Blueprint("specialization", __name__)



@specialization_bp.route('/sync', methods=['POST'])
def sync_specialization():
    specializations = Specialization.query.all()  
    for spec in specializations:
        es.index(index="specialization_index", id=spec.id, document={
            "name": spec.name,
            "description": spec.description
        })
    return jsonify({"message": "Specialization data synced successfully!"})