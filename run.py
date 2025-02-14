
from urllib import request
from app import create_app
from flask import render_template
from app.models import Doctor,Practice, db

# Create the app instance using the factory function
app = create_app()
from elasticsearch import Elasticsearch
es = Elasticsearch(["http://localhost:9200"])
from app.services.elasticsearch_service import search_doctors_in_es, search_practices_in_es


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
