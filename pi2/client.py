#!/usr/bin/env python

import time
import icinga2api.client as icinga2api


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

    def build_filters(self, object_type, object_name):
        """
        Return a filter
        """
        filters = {
            'type': object_type.title(),
            'filter': '{}.name=="{}"'.format(object_type, object_name),
            }
        return filters

    def schedule_host_downtime(self, client, host, comment, author, duration=600):
        """
        Schedule host downtime for duration
        """
        now = time.time()
    #   if isinstance(duration, str):
    #       duration = int(duration)
        end_time = now + duration
        filters = self.build_filters('host', host)
        task = client.actions.schedule_downtime(
            filters=filters,
            start_time=now,
            end_time=end_time,
            duration=duration,
            comment=comment,
            author=author,
        )
        return task
