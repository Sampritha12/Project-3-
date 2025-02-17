
from urllib import request
from app import create_app
from flask import render_template
from app.models import Doctor,Practice, db


app = create_app()
from elasticsearch import Elasticsearch
es = Elasticsearch(["http://localhost:9200"])
# from app.services.elasticsearch_service import search_doctors, search_practices
# try:
#     print(es.ping())  
# except Exception as e:
#     print(f"Connection error: {e}")


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
