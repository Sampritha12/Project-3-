from elasticsearch import Elasticsearch

# Initialize Elasticsearch connection
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}],
                   basic_auth=("elastic", "changeme"))

# Function to index a doctor in Elasticsearch
def index_doctor(doctor):
    document = {
        "name": doctor.name,
        "email": doctor.email,
        "qualifications": doctor.qualifications,
        "experience_years": doctor.experience_years,
        "specializations": [specialization.name for specialization in doctor.specializations],
        "description": doctor.description,
        "contact_number": doctor.contact_number,
    }
    es.index(index="doctors", id=doctor.id, body=document)

def index_practice(practice):
    document = {
        "name": practice.name,
        "city": practice.city,
        "address": practice.address,
        "contact_number": practice.contact_number,
        "email": practice.email,
        "specializations": [specialization.name for specialization in practice.specializations],
    }
    es.index(index="practices", id=practice.id, body=document)

# Function to search doctors in Elasticsearch
def search_doctors_in_es(name=None, specialization=None):
    query = {"bool": {"must": []}}

    if name:
        query["bool"]["must"].append({
            "match": {
                "name": {
                    "query": name,
                    "operator": "and"  
                }
            }
        })

    if specialization:
        query["bool"]["must"].append({
            "match": {
                "specializations": {
                    "query": specialization,
                    "operator": "and"
                }
            }
        })

    response = es.search(index="doctors", body={"query": query})

    doctors = []
    for hit in response['hits']['hits']:
        doctor = hit['_source']
        doctors.append({
            "id": hit['_id'],
            "name": doctor['name'],
            "email": doctor['email'],
            "qualifications": doctor['qualifications'],
            "experience_years": doctor['experience_years'],
            "specializations": doctor['specializations'],
            "description": doctor['description'],
            "contact_number": doctor['contact_number'],
        })

    return doctors

def search_practices_in_es(name=None, specialization=None):
    query = {"bool": {"must": []}}

    if name:
        query["bool"]["must"].append({
            "match": {
                "name": {
                    "query": name,
                    "operator": "and"
                }
            }
        })

    if specialization:
        query["bool"]["must"].append({
            "match": {
                "specializations": {
                    "query": specialization,
                    "operator": "and"
                }
            }
        })

    response = es.search(index="practices", body={"query": query})

    # Parse the search response to return practice data with full profile
    practices = []
    for hit in response['hits']['hits']:
        practice = hit['_source']
        practices.append({
            "id": hit['_id'],
            "name": practice['name'],
            "address": practice['address'],
            "city": practice['city'],
            "specializations": practice['specializations'],
            "doctors": practice.get('doctors', []),  # Handle missing field safely
            "contact_number": practice['contact_number'],
            "email": practice['email'],
            "website": practice.get('website', '')  # Handle missing field safely
        })

    return practices

# Function to search a doctor by ID in Elasticsearch
def search_doctor_by_id_in_es(doctor_id):
    response = es.get(index="doctors", id=doctor_id, ignore=404)
    return response["_source"] if response.get("found") else None

# Function to search a practice by ID in Elasticsearch
def search_practice_by_id_in_es(practice_id):
    response = es.get(index="practices", id=practice_id, ignore=404)
    return response["_source"] if response.get("found") else None
