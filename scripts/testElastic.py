#Code from: https://elasticsearch-py.readthedocs.io/en/v8.4.3/
from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch(hosts="https://localhost:9200", http_auth=("elastic","password"),verify_certs=False)

doc = {
    "type": "elasticsearch",
    "name": "car_db",
    "url": "databases-mariadb-people",
    "port": "9200",
    "usuario": "elastic",
    "password": "password"
}
resp = es.index(index="jobs", id=1, document=doc)
print(resp['result'])

resp = es.get(index="jobs", id=1)
print(resp['_source'])

es.indices.refresh(index="jobs")

resp = es.search(index="jobs", query={"match_all": {}})
print("Got %d Hits:" % resp['hits']['total']['value'])
for hit in resp['hits']['hits']:
    print("{ %(type)s\n  %(name)s\n  %(url)s\n  %(port)s\n  %(usuario)s\n  %(password)s }" % hit["_source"])