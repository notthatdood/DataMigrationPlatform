#code from https://www.rabbitmq.com/tutorials/tutorial-one-python.html
#Code from: https://elasticsearch-py.readthedocs.io/en/v8.4.3/
#!/usr/bin/env python
import json 
import time
import pika
import mariadb 
from elasticsearch import Elasticsearch
#Escuchar db de elasticSearch


def getTotalRegisters(expression, datasource, groupSize):
    #MariaDB connection
    conn = mariadb.connect(
    user="root",
    password="password",
    host="localhost",
    port=3306,
    database=datasource)
    cur = conn.cursor() 
    try: 
        cur.execute(expression) 
    except mariadb.Error as e: 
        print(f"Error: {e}")
    total=len(cur.fetchall())
    print("total registros: ", total)
    conn.close()
    return total // int(groupSize) + 1

def sendInfoToES(jobid, groupTotal, es):
    doc={
        "job_id": jobid,
        "group_id": jobid +"-"+ str(groupTotal)
    }
    resp = es.index(index="groups", id=1, document=doc)
    print(resp['result'])



def processJob(resp, es):
    for hit in resp['hits']['hits']:
        if hit["_source"]["status"]=="new":
            hit["_source"]["status"]="In-Progress"
            print("a document has changed to In-Progress status")
            print("----------------------------///////////////////////////////////=============================")
            doc=json.dumps(dict(hit["_source"]))
            resp = es.index(index="jobs", id=hit["_id"], document=doc)
            print(resp['result'])
            #Creo que esto es una caballada pero sirve
            total= getTotalRegisters(hit["_source"]["source"]["expression"], hit["_source"]["source"]["data_source"], hit["_source"]["source"]["grp_size"] )
            sendInfoToES(hit["_source"]["job_id"], total, es)
"""



channel.queue_declare(queue='regex_queue')
channel.queue_declare(queue='SQLProcessor_queue')

channel.basic_publish(exchange='', routing_key='regex_queue', body='pal regex queue')
channel.basic_publish(exchange='', routing_key='SQLProcessor_queue', body='pal SQL Processor queue')

connection.close()
"""




def main():
    #RabbitMQ connection
    #credentials = pika.PlainCredentials('user', 'password')
    #connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))
    #channel = connection.channel()
    #ES connection
    es = Elasticsearch(hosts="https://localhost:9200", http_auth=("elastic","password"),verify_certs=False)
    #Acquiring job table
    while(True):
        es.indices.refresh(index="jobs")
        resp = es.search(index="jobs", query={"match_all": {}})
        print("Got %d Hits:" % resp['hits']['total']['value'])
        processJob(dict(resp), es)
        time.sleep(20)
main()