from flask import Blueprint, request, jsonify,render_template
from app.models import Doctor, db
from app.services.elasticsearch_service import index_doctor, index_doctor_practice, index_practice, index_specializations, search_doctors
from elasticsearch import Elasticsearch



doctor_bp = Blueprint('doctor_bp', __name__)
es = Elasticsearch(["http://localhost:9200"])
DOCTOR_INDEX = "doctors"

@doctor_bp.route('/', methods=['GET'])
def get_doctor():
    name_query = request.args.get('name', default=None, type=str)
    
    if not name_query:
        doctors = search_doctors(name_query)
    else:
         doctors = es.search(index=DOCTOR_INDEX, body={"query": {"match_all": {}}})['hits']['hits']
    
    return jsonify([
    {
       "id": d["_id"],
        "name": d["_source"]["name"],
        "email": d["_source"]["email"],
        "qualifications": d["_source"]["qualifications"],
        "contact_number": d["_source"]["contact_number"],
        "description": d["_source"]["description"],  
        "experience_years": d["_source"]["experience_years"],
        "specialization": d["_source"]["specialization"] 


    }
    for d in doctors
])


@doctor_bp.route('/add', methods=['POST'])
def add_doctor():
    try:
        data = request.get_json()  
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400
        required_fields = ["name", "qualifications", "experience_years", "description", "contact_number", "email"]
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"Missing field: {field}"}), 400

        new_doctor = Doctor(
            name=data["name"],
            qualifications=data["qualifications"],
            experience_years=data["experience_years"],
            description=data["description"],
            contact_number=data["contact_number"],
            email=data["email"]
        )
        db.session.add(new_doctor)
        db.session.commit()

        try:
            index_doctor(new_doctor)
        except Exception as es_error:
            return jsonify({"error": f"Elasticsearch sync failed: {str(es_error)}"}), 500

        return jsonify({"message": "Doctor added successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@doctor_bp.route('/add_doctor', methods=['GET'])
def add_doctor_page():
    return render_template('add_doctor.html')



@doctor_bp.route('/sync', methods=['POST'])
def sync_doctors():
    try:
        doctors = Doctor.query.all()

        bulk_data = [
            {"_index": DOCTOR_INDEX, "_id": doctor.id, "_source": {
                "name": doctor.name,
                "qualifications": doctor.qualifications,
                "experience_years": doctor.experience_years,
                "description": doctor.description,
                "contact_number": doctor.contact_number,
                "email": doctor.email
            }} for doctor in doctors
        ]

        if not bulk_data:
            return jsonify({"message": "No doctors found to sync."})

        from elasticsearch.helpers import bulk
        bulk(es, bulk_data)

        return jsonify({"message": "Doctors synced successfully!"})

    except Exception as e:
        return jsonify({"error": f"Sync failed: {str(e)}"}), 500

