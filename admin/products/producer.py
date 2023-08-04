# amqps://rahhmdtg:ljZ0UUG1V8EAOMxNkYCOVI4TCloS9RXx@puffin.rmq2.cloudamqp.com/rahhmdtg

import pika, json

# params = pika.URLParameters('amqps://rahhmdtg:ljZ0UUG1V8EAOMxNkYCOVI4TCloS9RXx@puffin.rmq2.cloudamqp.com/rahhmdtg')

# connection = pika.BlockingConnection(params)

credentials = pika.PlainCredentials('rahhmdtg', 'ljZ0UUG1V8EAOMxNkYCOVI4TCloS9RXx')
parameters = pika.ConnectionParameters(
    host='puffin.rmq2.cloudamqp.com',
    virtual_host='rahhmdtg',
    credentials=credentials,
    heartbeat=0,
    # ssl=True  # Set to True for secure connections (e.g., using AMQPS)
)


connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='main')

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)
