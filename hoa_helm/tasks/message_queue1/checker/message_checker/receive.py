import sys

import pika
from pika.exceptions import AMQPError, ChannelClosedByBroker

CHANNEL = 'team1-task5'


def receive_message_and_exit():
    channel = None
    try:
        connection = pika.BlockingConnection()
        channel = connection.channel()
        method_frame, header_frame, body = channel.basic_get(CHANNEL)

        if method_frame:
            print("Got a message:", body, method_frame, header_frame, )
            channel.basic_ack(method_frame.delivery_tag)
            channel.close()
            sys.exit(0)

        print(f'No message returned from channel {CHANNEL}')
        channel.close()
        sys.exit(2)
    except ChannelClosedByBroker as exc:
        print(f"Could not open channel {CHANNEL}: {str(exc)}. Use `channel.queue_declare(...)` to create a queue.")
        sys.exit(3)
    except AMQPError:
        print("Unexpected error when connecting to Rabbit MQ")
        raise
    finally:
        if channel and channel.is_open:
            channel.close()


if __name__ == '__main__':
    receive_message_and_exit()
