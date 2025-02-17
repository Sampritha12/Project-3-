from elasticsearch import Elasticsearch
from app.models import Doctor, Practice ,Specialization,DoctorPractice,DoctorSpecialization,PracticeSpecialization

es = Elasticsearch(["http://localhost:9200"])
DOCTOR_INDEX = "doctors"
PRACTICE_INDEX = "practices"
SPECIALIZATION_INDEX = "specialization"
DOCTOR_SPECIALIZATION_INDEX = "doctor_specialization"
PRACTICE_SPECIALIZATION_INDEX = "practice_specialization"
DOCTOR_PRACTICE_INDEX = "doctor_practice"

doctor_mapping = {
    "mappings": {
        "properties": {
            "name": {"type": "text"},
            "qualifications": {"type": "text"},
            "experience_years": {"type": "integer"},
            "description": {"type": "text"},
            "contact_number": {"type": "keyword"},
            "email": {"type": "keyword"}
        }
    }
}

if not es.indices.exists(index=DOCTOR_INDEX):
    es.indices.create(index=DOCTOR_INDEX, mappings=doctor_mapping["mappings"])

practice_mapping = {
    "mappings": {
        "properties": {
            "name": {"type": "text"},
            "address": {"type": "text"},
            "city": {"type": "text"},
            "state": {"type": "text"},
            "contact_number": {"type": "keyword"},
            "email": {"type": "keyword"}
        }
    }
}

if not es.indices.exists(index=PRACTICE_INDEX):
    es.indices.create(index=PRACTICE_INDEX, body=practice_mapping)

def index_doctor(doctor):
    es.index(index=DOCTOR_INDEX, id=doctor.id, body={
        "name": doctor.name,
        "qualifications": doctor.qualifications,
        "experience_years": doctor.experience_years,
        "description": doctor.description,
        "contact_number": doctor.contact_number,
        "email": doctor.email
    },refresh="wait_for")
def search_doctors(name_query):
    query = {
        "query": {
            "wildcard": {
                "name": f"*{name_query}*"
            }
        }
    }
    response = es.search(index=DOCTOR_INDEX, body=query)
    return response['hits']['hits']

def index_practice(practice):
    es.index(index=PRACTICE_INDEX, id=practice.id, body={
        "name": practice.name,
        "address": practice.address,
        "city": practice.city,
        "state": practice.state,
        "contact_number": practice.contact_number,
        "email": practice.email
    })
def search_practices(query):
    response = es.search(index=PRACTICE_INDEX, body={
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["name", "address", "city", "state"]
            }
        }
    })
    return [hit["_source"] for hit in response['hits']['hits']]
def index_specializations():
    specializations = Specialization.query.all()
    
    for specialization in specializations:
        es.index(index="specialization_index", id=specialization.id, body={
            "id": specialization.id,
            "name": specialization.name,
            "description": specialization.description
        })
    
    print("Specializations indexed successfully!")


def index_doctor_practice():
    doctor_practices = db.session.execute("""
        SELECT dp.id, dp.doctor_id, dp.practice_id, dp.availability, dp.consultation_fee,
               d.name AS doctor_name, p.name AS practice_name
        FROM doctor_practice dp
        JOIN doctor d ON dp.doctor_id = d.id
        JOIN practice p ON dp.practice_id = p.id
    """).fetchall()

    for dp in doctor_practices:
        es.index(index="doctor_practice_index", id=dp.id, body={
            "id": dp.id,
            "doctor": {"id": dp.doctor_id, "name": dp.doctor_name},
            "practice": {"id": dp.practice_id, "name": dp.practice_name},
            "availability": dp.availability,
            "consultation_fee": dp.consultation_fee
        })
    
    print("Doctor-Practice relationships indexed successfully!")

def index_doctor_specialization():
    doctor_specializations = db.session.execute("""
        SELECT ds.id, ds.doctor_id, ds.specialization_id,
               d.name AS doctor_name, s.name AS specialization_name
        FROM doctor_specialization ds
        JOIN doctor d ON ds.doctor_id = d.id
        JOIN specialization s ON ds.specialization_id = s.id
    """).fetchall()

    for ds in doctor_specializations:
        es.index(index="doctor_specialization_index", id=ds.id, body={
            "id": ds.id,
            "doctor": {"id": ds.doctor_id, "name": ds.doctor_name},
            "specialization": {"id": ds.specialization_id, "name": ds.specialization_name}
        })
    
    print("Doctor-Specialization relationships indexed successfully!")

def index_practice_specialization():
    practice_specializations = db.session.execute("""
        SELECT ps.id, ps.practice_id, ps.specialization_id,
               p.name AS practice_name, s.name AS specialization_name
        FROM practice_specialization ps
        JOIN practice p ON ps.practice_id = p.id
        JOIN specialization s ON ps.specialization_id = s.id
    """).fetchall()

    for ps in practice_specializations:
        es.index(index="practice_specialization_index", id=ps.id, body={
            "id": ps.id,
            "practice": {"id": ps.practice_id, "name": ps.practice_name},
            "specialization": {"id": ps.specialization_id, "name": ps.specialization_name}
        })
    
    print("Practice-Specialization relationships indexed successfully!")

specialization_mapping = {
    "mappings": {
        "properties": {
            "name": {"type": "text"},
            "description": {"type": "text"}
        }
    }
}

doctor_specialization_mapping = {
    "mappings": {
        "properties": {
            "doctor_id": {"type": "integer"},
            "specialization_id": {"type": "integer"}
        }
    }
}

practice_specialization_mapping = {
    "mappings": {
        "properties": {
            "practice_id": {"type": "integer"},
            "specialization_id": {"type": "integer"}
        }
    }
}

doctor_practice_mapping = {
    "mappings": {
        "properties": {
            "doctor_id": {"type": "integer"},
            "practice_id": {"type": "integer"},
            "availability": {"type": "text"},
            "consultation_fee": {"type": "integer"}
        }
    }
}

if not es.indices.exists(index=SPECIALIZATION_INDEX):
    es.indices.create(index=SPECIALIZATION_INDEX, body=specialization_mapping)

if not es.indices.exists(index=DOCTOR_SPECIALIZATION_INDEX):
    es.indices.create(index=DOCTOR_SPECIALIZATION_INDEX, body=doctor_specialization_mapping)

if not es.indices.exists(index=PRACTICE_SPECIALIZATION_INDEX):
    es.indices.create(index=PRACTICE_SPECIALIZATION_INDEX, body=practice_specialization_mapping)

if not es.indices.exists(index=DOCTOR_PRACTICE_INDEX):
    es.indices.create(index=DOCTOR_PRACTICE_INDEX, body=doctor_practice_mapping)



