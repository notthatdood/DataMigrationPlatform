#code from https://www.rabbitmq.com/tutorials/tutorial-one-python.html
#code from https://github.com/prometheus/client_python
#!/usr/bin/env python
from concurrent.futures import process
from select import select
import pika, sys, os
import json
import pika
from elasticsearch import Elasticsearch
import mariadb 
from prometheus_client import start_http_server, Summary

#Create a metric in prometheus to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

def processJob(es,channel,connection, resp, job):
    job=job[2:]
    job=job[:len(job)-1]
    job = job.replace("'", "\"")
    job=json.loads(job)
    #this is to get the table
    for hit in resp["hits"]["hits"]:
        if hit["_source"]["job_id"] == job["job_id"]:
            datasource = hit["_source"]["source"]["data_source"]
            exp=hit["_source"]["source"]["expression"]
            grpSize=hit["_source"]["source"]["grp_size"]
            break
    conn = mariadb.connect(
    user="root",
    password="password",
    host="databases-mariadb",
    port=3306,
    database=datasource)
    cur = conn.cursor() 
    
    try: 
        cur.execute(exp + " LIMIT " + str(int(job["group_id"].split("-")[1]) -1) +", " + grpSize) 
    except mariadb.Error as e: 
        print(f"Error: {e}")
    selectList=cur.fetchall()
    try: 
        dbcommand=exp.split()        
        cur.execute("SHOW COLUMNS FROM "+datasource+"."+dbcommand[3]) 
    except mariadb.Error as e: 
        print(f"Error: {e}")
    #print("slist", selectList)
    columnList=cur.fetchall()
    #print("clist", columnList)
    docs=[]
    for document in selectList:
        doc={}
        fieldCounter = 0
        for columnName in columnList:
            doc[columnName[0]]=document[fieldCounter]
            fieldCounter += 1
        docs.append(doc)
    job["docs"]=docs
    conn.close()
    return job

def updateES(es, job):
    resp = es.search(index="groups", query={"match_all": {}})
    print("\n--------------------------------------------\n",resp["hits"]["hits"])
    for hit in resp["hits"]["hits"]:
        if hit["_source"]["job_id"]==job["job_id"]:
            resp = es.index(index="groups", id=hit["_id"] , document=job)
    #print(resp['_source'])

def sendToQueue(channel, doc, resp):
    for hit in resp['hits']['hits']:
        for stage1 in hit["_source"]["stages"]:
            if stage1["name"] == "extract":
                for stage2 in hit["_source"]["stages"]:
                    if stage2["name"] == "transform":
                        for transformation in stage2['transformation']:
                            if transformation['name'] in stage1['destination_queue']:
                                q = transformation['source_queue']
                                doc=doc[2:]
                                doc=doc[:len(doc)-1]
                                doc = doc.replace("'", "\"")
                                channel.queue_declare(queue=q)
                                channel.basic_publish(exchange='', routing_key= q , body=doc)
                                print(doc)
                                print("Sent to queue", q)
                                return
    
# Decorate function with metric.
@REQUEST_TIME.time()
def main():
    #RabbitMQ connection
    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(pika.ConnectionParameters('components-rabbitmq',5672,'/',credentials))
    channel = connection.channel()
    #ES connection
    es = Elasticsearch(hosts="https://databases-elasticsearch:9200", http_auth=("elastic","password"),verify_certs=False)

    channel.queue_declare(queue='extract')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        es.indices.refresh(index="jobs")
        resp = es.search(index="jobs", query={"match_all": {}})
        print("Got %d Hits:" % resp['hits']['total']['value'])
        job = processJob(es, channel, connection, dict(resp), str(body))
        updateES(es, job)
        sendToQueue(channel, str(body), resp)



    channel.basic_consume(queue='extract', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        # Start up the server to expose the metrics.
        start_http_server(8000)
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)