from flask import Blueprint, request, jsonify,render_template
from app.models import Practice, db
from app.services.elasticsearch_service import PRACTICE_INDEX, index_practice, search_practices

practice_bp = Blueprint('practice_bp', __name__)

@practice_bp.route('/', methods=['GET'])
def get_practice():
    name_query = request.args.get('name', default=None, type=str)
    
    if not name_query:
        practices = search_practices(name_query)
    else:
        practices = es.search(index=PRACTICE_INDEX, body={
            "query": {
                "wildcard": {
                    "name": f"*{name_query}*"
                }
            }
        })['hits']['hits']
    
    return jsonify([
        {"id": p.id, "name": p.name, "city": p.city, "address": p.address, 
      "state": p.state, "contact_number": p.contact_number, "email": p.email}
        for p in practices
    ])

@practice_bp.route('/add', methods=['POST'])
def add_practice():
    data = request.json
   
    new_practice = Practice(
        name=data['name'],
        address=data['address'],
        city=data['city'],
        state=data['state'],
        contact_number=data['contact_number'],
        email=data['email']
    )
    db.session.add(new_practice)
    db.session.commit()
    index_practice(new_practice)

    return jsonify({"message": "Practice added successfully"})
@practice_bp.route('/add_practice', methods=['GET'])
def add_practice_page():
    return render_template('add_practice.html')


@practice_bp.route('/sync', methods=['POST'])
def sync_practices():
    practices = Practice.query.all()
    for practice in practices:
        index_practice(practice)
    return jsonify({"message": "Practices synced successfully with Elasticsearch"})

