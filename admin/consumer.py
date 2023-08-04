# amqps://rahhmdtg:ljZ0UUG1V8EAOMxNkYCOVI4TCloS9RXx@puffin.rmq2.cloudamqp.com/rahhmdtg

import pika, json, os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE","admin.settings")
django.setup()

from products.models import Product

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

channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print('Received in admin',properties.content_type)

    if properties.content_type == 'product_liked':
        id = json.loads(body)
        print(id)
        product = Product.objects.get(id=id)
        product.likes = product.likes + 1
        print('after update',product)
        product.save()
        print('Product likes increased!')

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)


print('Started Consuming')

channel.start_consuming()

channel.close()