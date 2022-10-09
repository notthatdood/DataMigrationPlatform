#code from https://www.rabbitmq.com/tutorials/tutorial-one-python.html
#Code from: https://elasticsearch-py.readthedocs.io/en/v8.4.3/
#!/usr/bin/env python
import json 
from elasticsearch import Elasticsearch
#Escuchar db de elasticSearch
es = Elasticsearch(hosts="https://localhost:9200", http_auth=("elastic","password"),verify_certs=False)



es.indices.refresh(index="jobs")

resp = es.search(index="jobs", query={"match_all": {}})

print("Got %d Hits:" % resp['hits']['total']['value'])


for hit in resp['hits']['hits']:
    if hit["_source"]["status"]=="new":
        hit["_source"]["status"]="In-Progress"
        print("a document has changed to In-Progress status")
        print("----------------------------///////////////////////////////////=============================")
        doc=json.dumps(dict(hit["_source"]))
        resp = es.index(index="jobs", id=hit["_id"], document=doc)
        print(resp['result'])

es.indices.refresh(index="jobs")

resp = es.search(index="jobs", query={"match_all": {}})

print(resp["hits"]["hits"])


"""
import pika

credentials = pika.PlainCredentials('user', 'password')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))
channel = connection.channel()

channel.queue_declare(queue='regex_queue')
channel.queue_declare(queue='SQLProcessor_queue')

channel.basic_publish(exchange='', routing_key='regex_queue', body='pal regex queue')
channel.basic_publish(exchange='', routing_key='SQLProcessor_queue', body='pal SQL Processor queue')

connection.close()
"""




