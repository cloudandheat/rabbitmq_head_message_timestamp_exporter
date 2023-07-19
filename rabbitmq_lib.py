"""
Inhere you can find all rabbitmq related functions.
"""
import pika
import json
import ast

def get_broker_connection(host, user, password):
    credentials = pika.PlainCredentials(user, password)
    parameter = pika.ConnectionParameters(
        host=host,
        credentials=credentials,
    )
    connection = pika.BlockingConnection(parameter)
    return connection

def get_channel(connection):
    channel = connection.channel()
    return channel

def get_messages(host, user, password, queue, on_message_callback=None):
    connection = get_broker_connection(host, user, password)
    channel = get_channel(connection)

    if not on_message_callback:
        def on_message_callback(ch, method, properties, body):
            print(ch)
            print(method)
            print(properties)
            print(" [x] Received %r" % body)

    channel.basic_consume(queue=queue,
                          on_message_callback=on_message_callback,
                          auto_ack=False
                          )

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

def get_oslo_message(message):
    message_dict = json.loads(message)
    print(message_dict)
    oslo_message = ast.literal_eval(message_dict['oslo.message'])
    return oslo_message


def get_message_timestamp(message):
    oslo_message = get_oslo_message(message)
    timestamp = oslo_message['timestamp']
    return timestamp

def get_message_payload(message):
    oslo_message = get_oslo_message(message)
    payload = oslo_message['payload']
    return payload