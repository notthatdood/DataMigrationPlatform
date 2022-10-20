#code from https://www.rabbitmq.com/tutorials/tutorial-one-python.html
#Code from: https://elasticsearch-py.readthedocs.io/en/v8.4.3/
#!/usr/bin/env python
import json 
import time
import pika
import mariadb 
from elasticsearch import Elasticsearch
#Escuchar db de elasticSearch

#DATA=os.getenv('DATAFROMK8S')

RABBIT_MQ_HOST=os.getenv('RABBITMQHOST')
RABBIT_MQ_PASS=os.getenv('RABBITMQPASS')

SOURCE_QUEUE=os.getenv('SOURCEQUEUE')
DEST_QUEUE=os.getenv('DESTQUEUE')

ES_ENDPOINT=os.getenv('ESENDPOINT')
ES_PASSWORD=os.getenv('ESPASSWORD')
ES_INDEX=os.getenv('ESINDEX')

MDB_ENDPOINT=os.getenv('MDBENDPOINT')
MDB_PASSWORD=os.getenv('MDBPASSWORD')


def getTotalRegisters(expression, datasource, groupSize):
    #MariaDB connection
    conn = mariadb.connect(
    user="root",
    password="password",
    #password= MDB_PASSWORD,
    host="localhost",
    #host= MDB_ENDPOINT,
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

def sendInfoToESandRabbitMQ(q, jobid, groupTotal, es, channel, docId):
    doc={
        "job_id": jobid,
        "group_id": jobid +"-"+ str(groupTotal)
    }
    resp = es.index(index="groups", id=docId, document=doc)
    print(resp['result'])
    channel.queue_declare(queue=q)

    channel.basic_publish(exchange='', routing_key= q , body=json.dumps(doc))
    print("Sent to queue", q)



def processJob(resp, es, channel, connection):
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
            for stage in hit["_source"]["stages"]:
                if stage["name"] == "extract":
                    queue = stage["source_queue"]
                    sendInfoToESandRabbitMQ(queue, hit["_source"]["job_id"], total, es, channel, connection, hit['_id'])
                    break





def main():
    #RabbitMQ connection
    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))
    channel = connection.channel()
    #ES connection
    es = Elasticsearch(hosts="https://localhost:9200", http_auth=("elastic","password"),verify_certs=False)
    #Acquiring job table
    while(True):
        es.indices.refresh(index="jobs")
        resp = es.search(index="jobs", query={"match_all": {}})
        print("Got %d Hits:" % resp['hits']['total']['value'])
        processJob(dict(resp), es, channel, connection)
        time.sleep(20)
main()