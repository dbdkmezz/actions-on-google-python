# https://developers.google.com/actions/reference/rest/Shared.Types/AppRequest

import json
import pprint
import logging

from .exceptions import NoJsonException


logger = logging.getLogger(__name__)


class AppRequest(object):
    """Parses a request which has come from Google"""
    def __init__(self, request):
        self.text = None
        self.user_id = None
        self.conversation_id = None
        self.conversation_token = None

        self._parse_request(request)

    def _parse_request(self, request):
        body = request.body.decode('utf-8')
        try:
            j = json.loads(body)
        except json.JSONDecodeError:
            logger.warning('Unable to decode json, request body: "%s"', body)
            raise NoJsonException
        logger.debug('Request body: %s', pprint.pformat(j))

        self.conversation_id = j['conversation']['conversationId']
        self.conversation_token = j['conversation'].get('conversationToken')

        self.user_id = j['user']['userId']
        logger.debug('USER ID: %s', self.user_id)

        input = j['inputs'][0]
        if 'arguments' in input:
            self.text = input['arguments'][0]['textValue']
        else:
            logger.info('No arguments in request')
