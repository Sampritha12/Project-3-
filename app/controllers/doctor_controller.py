from flask import Blueprint, request, jsonify
from app.models import Doctor, db
from app.services.elasticsearch_service import index_doctor 

doctor_bp = Blueprint('doctor_bp', __name__)

@doctor_bp.route('/', methods=['GET'])
def get_doctor():
    name_query = request.args.get('name', default=None, type=str)
    
    if name_query:
        doctors = Doctor.query.filter(Doctor.name.ilike(f"%{name_query}%")).all()
    else:
        doctors = Doctor.query.all()
    
    return jsonify([
        {"id": d.id, "name": d.name, "email": d.email, "qualifications": d.qualifications} 
        for d in doctors
    ])

@doctor_bp.route('/add', methods=['POST'])
def add_doctor():
    data = request.json
    new_doctor = Doctor(
        name=data['name'], 
        qualifications=data['qualifications'],
        experience_years=data['experience_years'], 
        description=data['description'], 
        contact_number=data['contact_number'], 
        email=data['email']
    )
    db.session.add(new_doctor)
    db.session.commit()
    index_doctor(new_doctor)
    return jsonify({"message": "Doctor added successfully"})

# @doctor_bp.route('/<int:doctor_id>')
# def doctor_profile(doctor_id):
#     doctor = db.session.query(Doctor).get(doctor_id)  # Query with db.session
#     if not doctor:
#         abort(404)
#     return render_template('doctor_profile.html', doctor=doctor)

@doctor_bp.route('/search/doctors', methods=['GET'])
def search_doctors():
    name = request.args.get('name', '')

    # Query doctors whose names contain the search term (case-insensitive)
    doctors = Doctor.query.filter(Doctor.name.ilike(f"%{name}%")).all()

    return jsonify([
        {
            "id": d.id,
            "name": d.name,
            "email": d.email,
            "qualifications": d.qualifications
        } 
        for d in doctors
    ])

