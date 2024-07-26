CHANNEL = "team1-task5"
if __name__ == '__main__':
    import pika
    import pika.exceptions

    # Open a connection to RabbitMQ on localhost using all default parameters
    connection = pika.BlockingConnection()

    # Open the channel
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue=CHANNEL, durable=True, exclusive=False, auto_delete=False)

    # Enabled delivery confirmations. This is REQUIRED.
    channel.confirm_delivery()

    # Send a message
    try:
        channel.basic_publish(exchange='',
                              routing_key=CHANNEL,
                              body='Hello World!',
                              properties=pika.BasicProperties(content_type='text/plain',

                                                              delivery_mode=pika.DeliveryMode.Transient),
                              mandatory=True)
        print('Message was published')
    except pika.exceptions.UnroutableError:
        print('Message was returned')