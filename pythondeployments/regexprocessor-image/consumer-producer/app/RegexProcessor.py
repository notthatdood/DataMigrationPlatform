#code from https://www.rabbitmq.com/tutorials/tutorial-one-python.html
#Code from: https://elasticsearch-py.readthedocs.io/en/v8.4.3/
from elasticsearch import Elasticsearch
import re
import pika
import json


#Regular expression match logic
#txt = "Toyota Corollacross BWC-166, Blanco Perlado"
#txt1 = "Honda CRV HUJ-987, Dorado"
#Returns a list with the match
##Parameters need to be replaced by the ones provided on the job file.
#x = re.findall("^.*([a-zA-z]{3}-[0-9]{3}).*$", txt)
#x1 = re.findall("^.*([a-zA-z]{3}-[0-9]{3}).*$", txt1)
#print(x,x1)

def executeRegEx(job, es, regEx, group, field, objectiveField):
    #TODO: falta agregar la validación de group
    resp = es.search(index="groups", query={"match_all": {}})
    for hit in resp["hits"]["hits"]:
        if hit["_source"]["group_id"]==job["group_id"]:
            for doc in hit['_source']['docs']:
                try:
                    #Me volé todos los espacios del regex expression por que solo así me funcionaba
                    regEx=regEx.replace(" ", "")
                    print("regex: ", regEx)
                    print("description ", doc["description"])
                    print("result", re.findall(regEx, str(doc["description"])))
                    doc[objectiveField] = re.findall(regEx, str(doc["description"]))[0]
                    hit["_source"]["docs"][int(doc['id']) - 1]=doc
                except:
                    print("This document didn't have the required field: ", field)

    resp = es.index(index="groups", id=hit["_id"], document=hit["_source"])


def processJob(resp, es, job, channel):
    job = job[2:]
    job = job[:len(job)-1]
    job = job.replace("'", "\"")
    job=json.loads(job)
    for hit in resp['hits']['hits']:
        if hit["_source"]["job_id"]==job["job_id"]:
            for stage in hit["_source"]['stages']: 
                if stage['name']=='transform': 
                    for transformation in stage['transformation']:
                        if transformation['type']=='regex_transform':
                            regEx = transformation["regex_config"]["regex_expression"]
                            field = transformation["regex_config"]["field"]
                            group = transformation["regex_config"]["group"]
                            objectiveField = transformation["field_name"]
                            executeRegEx(job, es, str(regEx), group, field, objectiveField)

                            for stage2 in hit["_source"]['stages']:
                                #Enviamos el mensaje al queue correspondiente
                                #Busca que el nombre del queue coincida con el nombre indica
                                if stage2['name'] in transformation['destination_queue']:
                                    q = stage2['source_queue']
                                    channel.queue_declare(queue = q)
                                    channel.basic_publish(exchange='', routing_key= q, body=json.dumps(job))
                                    print("Sent to queue", q)
                            break


def main():
    #RabbitMQ connection
    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))
    channel = connection.channel()
    #ES connection
    es = Elasticsearch(hosts="https://localhost:9200", http_auth=("elastic","password"),verify_certs=False)

    channel.queue_declare(queue='regex_queue')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        es.indices.refresh(index="jobs")
        resp = es.search(index="jobs", query={"match_all": {}})
        print("Got %d Hits:" % resp['hits']['total']['value'])
        processJob(dict(resp), es, str(body), channel)


    channel.basic_consume(queue='regex_queue', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

main()
