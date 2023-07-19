import sys, os
import argparse
from rabbitmq_lib import get_messages

def main(args):
    mq_host = args.mq_host
    exporter_port = args.exporter_port
    user = args.user
    password = args.password
    queue = args.queue
    get_messages(mq_host, user, password, queue)

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
