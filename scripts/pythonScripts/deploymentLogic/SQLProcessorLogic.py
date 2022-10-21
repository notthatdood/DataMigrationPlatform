#Code from: https://elasticsearch-py.readthedocs.io/en/v8.4.3/
import pika, sys, os
import json
import mariadb 
from elasticsearch import Elasticsearch
import urllib3

#Disabling warnings because we are not using certificates
urllib3.disable_warnings()

#Takes the sql query with the replaced values and queries the mariadb
def executeSQLExpression(exp, datasource, job, es, channel):
    conn = mariadb.connect(
        user="root",
        password="password",
        host="localhost",
        port=3306,
        database=datasource
        )
    cur = conn.cursor() 
    resp = es.search(index="groups", query={"match_all": {}})
    for hit in resp["hits"]["hits"]:
        if hit["_source"]["group_id"]==job["group_id"]:
            for doc in hit['_source']['docs']:
                replacedExpression = exp.replace("%{doc_field}%",str(doc['id']))
                try:
                    print("replaced expression: ",replacedExpression) 
                    cur.execute(replacedExpression) 
                except mariadb.Error as e: 
                    print(f"Error: {e}")
                for row in cur: 
                    #Here we will be updating the groups index
                    row=row[0]
                    #row=row[:len(row)-2]
                    doc["description"]=row
                    hit["_source"]["docs"][int(doc['id']) - 1]=doc
    resp = es.index(index="groups", id=hit["_id"], document=hit["_source"])

#Receives the job, changes the query and calls executeSQLExpression to query mariadb 
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
                        if transformation['type']=='sql_transform':
                            keyList=list(transformation["fields_mapping"].keys())
                            replacedExpression = str(transformation["expression"])
                            #here we will replace the necessary strings
                            #print("to replace: " + "%{table}%")
                            replacedExpression = replacedExpression.replace("%{table}%",transformation["table"])

                            #this iterates through the fields that will be replaced
                            for key in keyList:
                                print("to replace: " + "%{"+key+"}%")
                                replacedExpression = replacedExpression.replace("%{"+key+"}%",transformation["fields_mapping"][key])
                            print(replacedExpression)
                            
                            datasource = transformation['source_data_source']
                            grpSize=hit["_source"]["source"]["grp_size"]
                            replacedExpression=replacedExpression + " LIMIT " + str(int(job["group_id"].split("-")[1]) -1) +", " + grpSize

                            executeSQLExpression(replacedExpression, datasource, job, es, channel)

                            for transformation2 in stage['transformation']:
                                #Enviamos el mensaje al queue correspondiente
                                if transformation2['name'] in transformation['destination_queue']:
                                    q= transformation2['source_queue']
                                    channel.queue_declare(queue=q)
                                    channel.basic_publish(exchange='', routing_key= q, body=json.dumps(job))
                                    print("Sent to queue", q)
                            #Vamos a eliminar todos los transformations ya hechos para evitar que se repitan
                            #Es una opción pero si hay más de un grupo no sirve
                            break


def main():
    #RabbitMQ connection
    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/', credentials))
    channel = connection.channel()
    #ES connection
    es = Elasticsearch(hosts="https://localhost:9200", http_auth=("elastic","password"), verify_certs=False)

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