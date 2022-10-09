#code from https://www.rabbitmq.com/tutorials/tutorial-one-python.html
#!/usr/bin/env python
from concurrent.futures import process
from select import select
import pika, sys, os
import json
import pika
from elasticsearch import Elasticsearch
import mariadb 

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
    host="localhost",
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
    print("slist", selectList)
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
    #TODO: por alguna razón no sirve
    
    return job

def updateES(es, job):
    print(job)
    es.update(index="groups", document=job)
    print(resp['_source'])


def main():
    #RabbitMQ connection
    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))
    channel = connection.channel()
    #ES connection
    es = Elasticsearch(hosts="https://localhost:9200", http_auth=("elastic","password"),verify_certs=False)
    #Acquiring job table
    channel.queue_declare(queue='extract')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        es.indices.refresh(index="jobs")
        resp = es.search(index="jobs", query={"match_all": {}})
        print("Got %d Hits:" % resp['hits']['total']['value'])
        job = processJob(es, channel, connection, dict(resp), str(body))
        



    channel.basic_consume(queue='extract', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)