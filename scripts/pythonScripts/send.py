#code from https://www.rabbitmq.com/tutorials/tutorial-one-python.html
#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('user', 'password')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))
channel = connection.channel()

channel.queue_declare(queue='sql_queue')

channel.basic_publish(exchange='', routing_key='sql_queue', body="{'job_id': 'job606', 'group_id': 'job606-1'}")
print(" [x] Sent'")
connection.close()