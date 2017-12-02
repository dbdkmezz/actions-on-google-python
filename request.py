import json
import pprint
import logging

from .exceptions import NoJsonException


class GoogleRequest(object):
    """Parses a request which has come from Google"""
    def __init__(self, request, logger=logging.getLogger()):
        self.logger = logger
        self._parse_request(request)

    def _parse_request(self, request):
        self.text = None
        self.user_id = None

        body = request.body.decode('utf-8')
        self.logger.info('Request body: %s', pprint.pformat(body))
        try:
            j = json.loads(body)
        except json.JSONDecodeError:
            self.logger.warn('Unable to decode json')
            raise NoJsonException

        self.user_id = j['user']['userId']
        self.logger.info('USER ID: %s', self.user_id)
        input = j['inputs'][0]

        if 'arguments' not in input:
            self.logger.info('No arguments in request')
            return None

        self.text = input['arguments'][0]['textValue']
