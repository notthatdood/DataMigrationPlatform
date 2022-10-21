#code from https://www.rabbitmq.com/tutorials/tutorial-one-python.html
#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('user', 'password')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))
channel = connection.channel()

channel.queue_declare(queue='extract')

channel.basic_publish(exchange='', routing_key='extract', body="{'job_id': 'job606', 'group_id': 'job606-1'}")
print(" [x] Sent'")
connection.close()