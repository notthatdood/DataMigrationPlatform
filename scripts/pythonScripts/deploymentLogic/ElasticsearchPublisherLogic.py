#Code from https://www.rabbitmq.com/tutorials/tutorial-one-python.html
#Code from: https://elasticsearch-py.readthedocs.io/en/v8.4.3/
import pika, sys, os
import json
from elasticsearch import Elasticsearch





#Procesa el grupo y lo agrega al destination data source indicado en el json
def processGroup(resp, es, job, destination_data_source, destination_index):
    resp = es.search(index="groups", query={"match_all": {}})
    for hit in resp["hits"]["hits"]:
        if hit["_source"]["group_id"]==job["group_id"]:
            for doc in hit['_source']['docs']:
                #TODO: should specify the desired database as well
                print("destination db", destination_data_source)
                print("destination index", destination_index)
                es.index(index = destination_index, document=doc)


#Receives the job, changes the query and calls executeSQLExpression to query mariadb 
def processJob(resp, es, job):
    job = job[2:]
    job = job[:len(job)-1]
    job = job.replace("'", "\"")
    job=json.loads(job)
    for hit in resp['hits']['hits']:
        if hit["_source"]["job_id"]==job["job_id"]:
            for stage in hit["_source"]['stages']: 
                if stage['name']=='load': 
                    processGroup(resp, es, job,stage["destination_data_source"], stage["index_name"])
                    break


def main():
    #RabbitMQ connection
    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))
    channel = connection.channel()
    #ES connection
    es = Elasticsearch(hosts="https://localhost:9200", http_auth=("elastic","password"),verify_certs=False)

    channel.queue_declare(queue='ready')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        es.indices.refresh(index="jobs")
        resp = es.search(index="jobs", query={"match_all": {}})
        print("Got %d Hits:" % resp['hits']['total']['value'])
        processJob(dict(resp), es, str(body))



    channel.basic_consume(queue='ready', on_message_callback=callback, auto_ack=True)

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