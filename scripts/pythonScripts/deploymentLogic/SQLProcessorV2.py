#Code from: https://elasticsearch-py.readthedocs.io/en/v8.4.3/
import pika, sys, os
from elasticsearch import Elasticsearch

def processJob(resp, es):
    for hit in resp['hits']['hits']:
        for stage in hit['stages']: 
            if stage['name']=='transform': 
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

def main():
    #RabbitMQ connection
    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))
    channel = connection.channel()
    #ES connection
    es = Elasticsearch(hosts="https://localhost:9200", http_auth=("elastic","password"),verify_certs=False)

    channel.queue_declare(queue='sql_queue')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        es.indices.refresh(index="jobs")
        resp = es.search(index="jobs", query={"match_all": {}})
        print("Got %d Hits:" % resp['hits']['total']['value'])
        processJob(dict(resp), es)
        



    channel.basic_consume(queue='extract', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
print("------------------------------------------------------------------\n")
