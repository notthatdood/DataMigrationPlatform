import time
import os
import sys
import pika

DATA=os.getenv('DATAFROMK8S')
RABBIT_MQ=os.getenv('RABBITMQ')
RABBIT_MQ_PASSWORD=os.getenv('RABBITPASS')
QUEUE_NAME=os.getenv('RABBITQUEUE')

credentials = pika.PlainCredentials('user', RABBIT_MQ_PASSWORD)
parameters = pika.ConnectionParameters(host=RABBIT_MQ, credentials=credentials)
connection = pika.BlockingConnection(parameters)
#connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)


channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()