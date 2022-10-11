from elasticsearch import Elasticsearch
import re
import pika
import json


#Regular expression match logic
txt = "Toyota Corollacross BWC-166, Blanco Perlado"
txt1 = "Honda CRV HUJ-987, Dorado"

#Returns a list with the match
#Parameters need to be replaced by the ones provided on the job file.
x = re.findall("^.*([a-zA-z]{3}-[0-9]{3}).*$", txt)
x1 = re.findall("^.*([a-zA-z]{3}-[0-9]{3}).*$", txt1)
print(x,x1)


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
                        if transformation['type']=='regex_transform':
                            transformationCount += 1
                            
                            
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

#Falta de terminar, lógica de reemplazo es la misma que la de SQL Processor