import traceback
from time import sleep
import pika.exceptions

CHANNEL = "team1-task5"
if __name__ == '__main__':
    
    parameters = pika.ConnectionParameters()
    # Open a connection to RabbitMQ on localhost using all default parameters

    print(f"Trying to connect to {parameters}")
    connection = pika.BlockingConnection(parameters=parameters)
    print(f"Success! Connected to {connection}")

    # Open the channel
    channel = connection.channel()

    # Enabled delivery confirmations. This is REQUIRED.
    channel.confirm_delivery()

    # Send a message
    while True:
        try:
            channel.basic_publish(exchange='',
                                  routing_key=CHANNEL,
                                  body='Hello World!',
                                  properties=pika.BasicProperties(content_type='text/plain',
                                                                  delivery_mode=pika.DeliveryMode.Transient),
                                  mandatory=True
                                  )
            print('Message was published.')
        except pika.exceptions.AMQPChannelError as ex:
            print(f'Message was returned: {str(ex)}')
        finally:
            sleep(30)
