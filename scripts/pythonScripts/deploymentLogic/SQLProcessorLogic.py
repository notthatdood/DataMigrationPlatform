#Code from: https://elasticsearch-py.readthedocs.io/en/v8.4.3/
import pika, sys, os
import json
from elasticsearch import Elasticsearch


def processJob(resp, es, job, channel):
    job=job[2:]
    job=job[:len(job)-1]
    job = job.replace("'", "\"")
    job=json.loads(job)
    print(job)
    #perdón por la chanchada profe
    hitCount =-1
    for hit in resp['hits']['hits']:
        hitCount+=1
        stageCount=-1
        if hit["_source"]["job_id"]==job["job_id"]:
            for stage in hit["_source"]['stages']: 
                stageCount += 1
                if stage['name']=='transform': 
                    transformationCount =- 1
                    for transformation in stage['transformation']:
                        if transformation['type']=='sql_transform':
                            transformationCount += 1
                            keyList=list(transformation["fields_mapping"].keys())
                            replacedExpression = str(transformation["expression"])
                            #here we will replace the necessary strings
                            print("to replace: " + "%{doc_field}%")
                            replacedExpression = replacedExpression.replace("%{doc_field}%",transformation["doc_field"])
                            print("to replace: " + "%{table}%")
                            replacedExpression = replacedExpression.replace("%{table}%",transformation["table"])
                            #this iterates through the fields that will be replaced
                            for key in keyList:
                                print("to replace: " + "%{"+key+"}%")
                                replacedExpression = replacedExpression.replace("%{"+key+"}%",transformation["fields_mapping"][key])
                            print(replacedExpression)
                            
                            for transformation2 in stage['transformation']:
                                if transformation2['name'] in transformation['destination_queue']:
                                    channel.basic_publish(exchange='', routing_key= transformation2['source_queue'] , body=json.dumps(job))
                            #Vamos a eliminar todos los transformations ya hechos para evitar que se repitan
                            #Es una opción pero si hay más de un grupo no sirve
                            #del hit["_source"]['stages'][stageCount]['transformation'][transformationCount] 
                            #print(hit["_source"])
                            #es.index(index="jobs",id=hit["_id"], body=hit["_source"])
                            break

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
        processJob(dict(resp), es, str(body), channel)


    channel.basic_consume(queue='sql_queue', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

main()
