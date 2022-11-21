from elasticsearch import Elasticsearch
es = Elasticsearch(hosts="https://localhost:9200", basic_auth=("elastic","password"),verify_certs=False)
"""
resp = es.get(index="jobs", id=1)
print(resp['_source'])

es.indices.refresh(index="jobs")

resp = es.search(index="jobs", query={"match_all": {}})
print("Got %d Hits:" % resp['hits']['total']['value'])
for hit in resp['hits']['hits']:
    print(hit, "\n-----------------------------------------------")
"""

resp = es.search(index="persona", query={"match_all": {}})
#print(resp["hits"]["hits"])
for hit in resp["hits"]["hits"]:
    print(hit["_source"])