from flask import Blueprint, request, jsonify
from app.models import Doctor, DoctorPractice, Practice, db
from app.services.elasticsearch_service import index_practice 

practice_bp = Blueprint('practice_bp', __name__)

@practice_bp.route('/', methods=['GET'])
def get_practices():
    name_query = request.args.get('name', default=None, type=str)
    
    if name_query:
        practices = Practice.query.filter(Practice.name.ilike(f"%{name_query}%")).all()
    else:
        practices = Practice.query.all()

    return jsonify([
        {"id": p.id, "name": p.name, "city": p.city, "address": p.address, 
         "state": p.state, "contact_number": p.contact_number, "email": p.email} 
        for p in practices
    ])

# Add new practice
@practice_bp.route('/add', methods=['POST'])
def add_practice():
    data = request.json
    new_practice = Practice(
        name=data['name'],
        address=data['address'],
        city=data['city'],
        state=data['state'],
        contact_number=data['contact_number'],
        email=data['email'],
    )
    db.session.add(new_practice)
    db.session.commit()
    index_practice(new_practice)
    return jsonify({"message": "Practice added successfully"})


@practice_bp.route('/<int:practice_id>/doctors', methods=['GET'])
def get_doctors_for_practice(practice_id):
    doctor_practices = db.session.query(DoctorPractice).filter_by(practice_id=practice_id).all()
    doctor_ids = [dp.doctor_id for dp in doctor_practices]
    doctors = Doctor.query.filter(Doctor.id.in_(doctor_ids)).all()

    return jsonify([
        {"id": d.id, "name": d.name, "email": d.email, "qualifications": d.qualifications, 
         "availability": next((dp.availability for dp in doctor_practices if dp.doctor_id == d.id), ""),
         "consultation_fee": next((dp.consultation_fee for dp in doctor_practices if dp.doctor_id == d.id), "")}
        for d in doctors
    ])


