#!/usr/bin/env python

import argparse
import pi2c
import json


def get_args():
    """
    Get arguments
    """
    parser = argparse.ArgumentParser(description='Set downtime with icinga2')

    parser.add_argument('-H', '--host',
                        action='store',
                        help='Host to set downtime for')

    parser.add_argument('-s', '--server',
                        action='store',
                        help='Icinga server to connect to',
                        default='https://icinga-master01-prod.ops.puppetlabs.net')

    parser.add_argument('-u', '--user',
                        action='store',
                        help='API user to connect with for icinga2api',
                        default='icinga2')

    parser.add_argument('-p', '--password',
                        required=True,
                        action='store',
                        help='Password for API user')

    parser.add_argument('-P', '--port',
                        action='store',
                        default=5665,
                        help='Port for connecting')

    parser.add_argument('-c', '--comment',
                        action='store',
                        default='downtime',
                        help='Comment for downtime')

    parser.add_argument('-d', '--duration',
                        action='store',
                        default=600,
                        type=int,
                        help='Duration for downtime, in seconds (default: 600s)')

    parser.add_argument('-a', '--author',
                        action='store',
                        default='icinga2',
                        help='Author of downtime')

    parser.add_argument('-S', '--service',
                        action='store',
                        help='Name of service to set downtime for')

    parser.add_argument('-f', '--filter',
                        action='store',
                        type=json.loads,
                        help='Icinga2 filter. Overrides service and host.')

    args = parser.parse_args()
    return args


def main():
    try:
        c = pi2c.client.Client()
        args = get_args()
        connection = c.open_connection(
            args.server, args.user, args.password)
        if args.filter:
            set_downtime = c.schedule_downtime(
                connection, args.filter, args.comment, args.author, args.duration)
        elif args.service:
            set_downtime = c.schedule_service_downtime(
                connection, args.comment, args.author, args.duration, args.service, args.host)
        else:
            set_downtime = c.schedule_host_downtime(
                connection, args.host, args.comment, args.author, args.duration)
        if set_downtime:
            if args.filter:
                result = 'Successfully set downtime with {} filter {}'.format(
                    args.filter['type'].lower(), args.filter['filter'])
            elif args.service:
                result = 'Successfully set downtime for {} instances of {}'.format(
                    len(set_downtime), args.service)
            else:
                result = 'Successfully set downtime for {}'.format(args.host)
        else:
            if args.filter:
                result = 'Cannot set downtime with {} filter {}'.format(
                    args.filter['type'], args.filter['filter'])
            else:
                result = 'Cannot set downtime'
        print result
    except:
        raise

if __name__ == '__main__':
    main()
