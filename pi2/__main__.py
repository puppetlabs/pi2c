#!/usr/bin/env python

import argparse
import pi2


def get_args():
    """
    Get arguments
    """
    parser = argparse.ArgumentParser(description='Set downtime with icinga2')

    parser.add_argument('-H', '--host',
                        required=True,
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
                        help='Duration for downtime')

    parser.add_argument('-a', '--author',
                        action='store',
                        default='icinga2',
                        help='Author of downtime')

    args = parser.parse_args()
    return args


def main():
    try:
        c = pi2.client.Client()
        args = get_args()
        connection = c.open_connection(
            args.server, args.user, args.password)
        set_downtime = c.schedule_host_downtime(
            connection, args.host, args.comment, args.author, args.duration)
        if len(set_downtime['results']) == 1:
            if set_downtime['results'][0]['code'] == 200.0:
                result = set_downtime['results'][0]['status']
            else:
                result = 'Cannot set downtime for {}. Received code {}'.format(
                    args.host, set_downtime['results'][0]['code'])
        else:
            result = 'Cannot set downtime for {}'.format(args.host)
        print result
    except:
        raise

if __name__ == '__main__':
    main()
