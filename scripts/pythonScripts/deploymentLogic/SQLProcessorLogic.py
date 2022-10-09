#Code from: https://elasticsearch-py.readthedocs.io/en/v8.4.3/
from elasticsearch import Elasticsearch


es = Elasticsearch(hosts="https://localhost:9200", http_auth=("elastic","password"),verify_certs=False)

doc = {
    "name": "add_car",
    "type": "sql_transform",
    "table": "car",
    "expression": "SELECT %{field_description}% FROM %{table}% WHERE %{field_owner}% = %{doc_field}%",
    "source_data_source": "database_car",
    "destination_data_source": "destination_es",
    "doc_field": "id",
    "source_queue": "sql_queue",
    "destination_queue": "%{transform->transformation->myregex}%",
    "fields_mapping": {
        "field_description": "description",
        "field_owner": "owner",
    }
}
#resp = es.index(index="jobs", id=2, document=doc)
#print(resp['result'])

resp = es.get(index="jobs", id=1)
print(resp['_source'])

es.indices.refresh(index="jobs")

resp = es.search(index="jobs", query={"match_all": {}})
print("Got %d Hits:" % resp['hits']['total']['value'])
for hit in resp['hits']['hits']:
    keyList=list(hit["_source"]["fields_mapping"].keys())
    replacedExpression = str(hit["_source"]["expression"])
    #here we will replace the necessary strings
    print("to replace: " + "%{doc_field}%")
    replacedExpression = replacedExpression.replace("%{doc_field}%",hit["_source"]["doc_field"])
    print("to replace: " + "%{table}%")
    replacedExpression = replacedExpression.replace("%{table}%",hit["_source"]["table"])
    #this iterates through the fields that will be replaced
    for key in keyList:
        print("to replace: " + "%{"+key+"}%")
        replacedExpression = replacedExpression.replace("%{"+key+"}%",hit["_source"]["fields_mapping"][key])
    print(replacedExpression)
    
    



print("------------------------------------------------------------------\n")
