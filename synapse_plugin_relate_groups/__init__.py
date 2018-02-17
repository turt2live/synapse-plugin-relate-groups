import json
import logging
import re
import requests


class RelateGroupsPlugin(object):
    def __init__(self, config, api):
        self._config = config
        self._api = api

    def on_room_directory_association_created(self, event):
        groups = []
        access_token = ""
        for r, c in self._config['groups'].iteritems():
            if r.match(event['room_alias']):
                for group_id, token in c.iteritems():
                    access_token = token
                    groups.append(group_id)

        if len(groups) <= 0:
            logging.info("[Groups Plugin] No groups to add for " + event['room_alias'])
        logging.info("[Groups Plugin] Updating groups for " + event['room_alias'])

        response = requests.request(
            "GET", self._config['homeserver_url'] + "/_matrix/client/r0/rooms/" + event['room_id'] + "/state/m.room.related_groups",
            params={"access_token": access_token},
        )
        current_groups = []
        if response.status_code == 200:
            current_groups = response.json()["groups"]
        logging.info("[Groups Plugin] Current groups for " + event['room_alias'] + " are %r", current_groups)

        for group_id in groups:
            if group_id in current_groups:
                continue
            current_groups.append(group_id)

        logging.info("[Groups Plugin] Setting groups for " + event['room_alias'] + " to %r", current_groups)
        response = requests.request(
            "PUT", self._config['homeserver_url'] + "/_matrix/client/r0/rooms/" + event['room_id'] + "/state/m.room.related_groups",
            params={"access_token": access_token},
            headers={"Content-Type": "application/json"},
            data=json.dumps({"groups": current_groups}),
        )
        logging.info("[Groups Plugin] Status code for update: %d" % response.status_code)

    @staticmethod
    def parse_config(config):
        if "homeserver_url" not in config:
            raise ValueError("Missing homeserver url")
        if "groups" not in config:
            raise ValueError("Missing homeserver url")

        remapped = {}
        expressions = {}
        for c in config['groups']:
            if "group_id" not in c:
                raise ValueError('Missing group ID')
            if "aliases" not in c:
                raise ValueError('Missing aliases for %s' % c['group_id'])
            if "access_token" not in c:
                raise ValueError('Missing access token for %s' % c['group_id'])

            for alias in c['aliases']:
                obj = {}
                r = re.compile(alias)
                if alias in expressions:
                    r = expressions[alias]
                    obj = remapped[r]
                obj[c['group_id']] = c['access_token']
                remapped[r] = obj

        return {
            "groups": remapped,
            "homeserver_url": config["homeserver_url"],
        }
