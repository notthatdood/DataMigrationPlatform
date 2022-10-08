import time
import os
import sys
import pika
import hashlib
import json
from datetime import datetime
from elasticsearch import Elasticsearch 

#definicion de la llamada asincronica
def callback(ch, method, properties, body):
    json_object = json.loads(body)
    resp = client.index(index = ESINDEX, id = hashlib.md5(body).hexdigest(), document = json_object) 
    #ese id es corrspondiente a su direccion
    print(resp)
    print(" [x] Received %r" % body)

DATA = os.getenv('DATAFROMK8S')
RABBIT_MQ = os.getenv('RABBITMQ')
RABBIT_MQ_PASSWORD = os.getenv('RABBITPASS')
QUEUE_NAME = os.getenv('RABBITQUEUE')
ES_ENDPOINT = os.getenv('ESENDPOINT')
ES_PASSWORD = os.getenv('ESPASSWORD')
ES_INDEX = os.getenv('ESINDEX')

client = Elasticsearch("https://" + ES_ENDPOINT + ":9200", basic_auth = ("elastic", ES_PASSWORD), verify_certs = False)
# creacion del cliente. !Las variables de entorno se deben jalar desde el secret 

credentials = pika.PlainCredentials('user', RABBIT_MQ_PASSWORD)
parameters = pika.ConnectionParameters(host = RABBIT_MQ, credentials = credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue = QUEUE_NAME)
channel.basic_consume(queue = QUEUE_NAME, on_message_callback = callback, auto_ack = True)
# el cliente da el OK antes de que todo este listo
print(" [x] Waiting for messages. To exit press CTRL + C")
channel.start_consuming()
# el proceso se queda bloqueado

