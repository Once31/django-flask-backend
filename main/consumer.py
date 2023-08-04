# amqps://rahhmdtg:ljZ0UUG1V8EAOMxNkYCOVI4TCloS9RXx@puffin.rmq2.cloudamqp.com/rahhmdtg

import pika, json

from main import Product, db

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


def callback(ch, method, properties, body):
    print('Received in main')
    data = json.loads(body) #convert data back json to normal
    print(data)

    if properties.content_type == "product_created":
        product = Product(id= data['id'],title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        print('product created')

    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
        print('product updated')

    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print('product deleted')

channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)


print('Started Consuming')

channel.start_consuming()

channel.close()