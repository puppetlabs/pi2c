#!/usr/bin/env python

import time
import icinga2api.client as icinga2api
from timeout import Timeout


class Client:
    """
    Interact with python-icinga2api library
    """
    def open_connection(self, server, user, password, port=5665):
        """
        Open connection to icinga2 server
        """
        server = server + ':' + str(port)
        client = icinga2api.Client(server, user, password)
        return client

    def host_filter(self, hostname):
        """
        Return a filter
        """
        filters = {
            'type': 'Host',
            'filter': 'host.name=="{}"'.format(hostname),
        }
        return filters

    def service_filter(self, servicename, hostname=None):
        """
        Return filter for Service type
        """
        filters = {'type': 'Service'}
        service_part = 'match("{}", service.name)'.format(servicename)
        if hostname:
            host_part = 'host.name=="{}"'.format(hostname)
            service_part = host_part + ' && ' + service_part
        filters['filter'] = service_part
        return filters

    def schedule_host_downtime(self, client, host, comment, author, duration=600, service_name='*'):
        """
        Schedule host downtime for duration
        """
        host_filter = self.host_filter(host)
        service_filter = self.service_filter(service_name, host)
        try_count = 0
        while try_count < 3:
            try:
                now = time.time()
                end_time = now + duration
                results = []
                for filters in [host_filter, service_filter]:
                    host_task = client.actions.schedule_downtime(
                        filters=filters,
                        start_time=now,
                        end_time=end_time,
                        duration=duration,
                        comment=comment,
                        author=author)
                    if len(host_task['results']) > 0:
                        for result in host_task['results']:
                            if result['code'] == 200.0:
                                results.append(result['status'])
                    else:
                        results = False
                        try_count = 3
                        break
                try_count = 3
            except Timeout.Timeout:
                results = "Operation timed out"
                print 'Timeout. Trying again'
        return results

    def schedule_service_downtime(self, client, comment, author,
                                  duration, service_name, host=None):
        """
        Schedule downtime for a service

        Filter on host if specified
        """
        service_filter = self.service_filter(service_name, host)
        try_count = 0
        while try_count < 3:
            try:
                now = time.time()
                end_time = now + duration
                results = []
                with Timeout(20):
                    try_count = try_count + 1
                    host_task = client.actions.schedule_downtime(
                        filters=service_filter,
                        start_time=now,
                        end_time=end_time,
                        duration=duration,
                        comment=comment,
                        author=author)
                    if len(host_task['results']) > 0:
                        for result in host_task['results']:
                            if result['code'] == 200.0:
                                results.append(result['status'])
                    else:
                        results = False
                    try_count = 3
            except Timeout.Timeout:
                results = "Operation timed out"
                print 'Timeout. Trying again'
        return results
