import os
import sys

import pika
from pika.exceptions import AMQPError, ChannelClosedByBroker


def receive_message_and_exit():
    channel = None
    rabbit_host = os.environ["RABBIT_HOST"]
    queue_name = os.environ["QUEUE_NAME"]
    try:
        parameters = pika.ConnectionParameters(host=rabbit_host)
        print(f"Trying to connect to {parameters}.")
        connection = pika.BlockingConnection(parameters=parameters)
        channel = connection.channel()
        print(f"Connecting to {queue_name}.")

        method_frame, header_frame, body = channel.basic_get(queue=queue_name)

        if method_frame:
            print("Got a message:", body, method_frame, header_frame, )
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            sys.exit(0)

        print(f'No message returned from channel {queue_name}')
        sys.exit(2)
    except ChannelClosedByBroker as exc:
        print(f"Could not open channel {queue_name}: {str(exc)}.\n")
        sys.exit(3)
    except AMQPError:
        print("Unexpected error when connecting to Rabbit MQ")
        raise
    finally:
        if channel and channel.is_open:
            channel.close()


if __name__ == '__main__':
    receive_message_and_exit()
