import sys, os
import argparse

from prometheus_client import start_http_server, Gauge
from datetime import datetime

from rabbitmq_lib import get_messages, get_message_timestamp, get_message_payload

TIMESTAMP_GAUGE = Gauge('message_timestamp', 'Time message was created')
GENERATED_GAUGE = Gauge('message_generated', 'Time message was generated')

def on_rabbit_message_callback(ch, method, properties, body):
    timestamp = get_message_timestamp(body)
    payload = get_message_payload(body)
    generated = payload[0]['generated']

    timestamp = datetime.strptime(timestamp,'%Y-%m-%d %H:%M:%S.%f' )
    generated = datetime.strptime(generated,'%Y-%m-%dT%H:%M:%S.%f' )

    total_timestamp = (timestamp - datetime(1970,1,1)).total_seconds()
    total_generated = (generated - datetime(1970,1,1)).total_seconds()

    print(total_timestamp)
    print(total_generated)
    TIMESTAMP_GAUGE.set(total_timestamp)
    GENERATED_GAUGE.set(total_generated)

def main(args):
    mq_host = args.mq_host
    exporter_port = args.exporter_port
    user = args.user
    password = args.password
    queue = args.queue

    # Start up the server to expose the metrics.
    start_http_server(exporter_port)

    get_messages(mq_host, user, password, queue, on_rabbit_message_callback)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    # comment in if using a config file is implemented
    # parser.add_argument('--config', '-c',
    #                     # type=argparse.FileType('r'),
    #                     dest='config_file',
    #                     default='settings.conf',
    #                     help='The config file to use'
    #                     )
    parser.add_argument('--mq-host', '-m',
                        dest='mq_host',
                        default='localhost')
    parser.add_argument('--exporter-port', '-e',
                        dest='exporter_port',
                        type=int,
                        default='8000')
    parser.add_argument('--queue', '-q',
                        dest='queue',
                        default='event.sample')
    parser.add_argument('--user', '-u',
                        dest='user',
                        default='stackrabbit')
    parser.add_argument('--pass', '-p',
                        dest='password',
                        default='secret')
    args = parser.parse_args()
    try:
        main(args)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)







