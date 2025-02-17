from app import db

class Specialization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    qualifications = db.Column(db.String(255))
    experience_years = db.Column(db.Integer)
    description = db.Column(db.Text)
    contact_number = db.Column(db.String(15))
    email = db.Column(db.String(255), unique=True)
    
class Practice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(15))
    email = db.Column(db.String(255), unique=True)
    
class DoctorSpecialization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    specialization_id = db.Column(db.Integer, db.ForeignKey('specialization.id'), nullable=False)

class PracticeSpecialization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    practice_id = db.Column(db.Integer, db.ForeignKey('practice.id'), nullable=False)
    specialization_id = db.Column(db.Integer, db.ForeignKey('specialization.id'), nullable=False)

class DoctorPractice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    practice_id = db.Column(db.Integer, db.ForeignKey('practice.id'), nullable=False)
    availability = db.Column(db.String(255), nullable=False)
    consultation_fee = db.Column(db.Numeric(10, 2), nullable=False)