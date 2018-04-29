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
        self.is_health_check = False

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
            arguments = self._arguments_with_names(input)
            self.text = self._get_text(arguments)
            self.is_health_check = self._is_health_check(arguments)
        else:
            logger.info('No arguments in request')

    @staticmethod
    def _arguments_with_names(input):
        return {a['name']: a for a in input['arguments']}

    @staticmethod
    def _get_text(arguments):
        text_argument_names = ['text', 'trigger_query']
        try:
            argument = next(
                v for k, v in arguments.items()
                if (k in text_argument_names))
        except StopIteration:
            return None

        if argument.get('rawText') != argument.get('textValue'):
            # Not sure what the difference between these two is, they always seem to be the same
            logger.error("rawText different from textValue, don't know why. Arguments: %s", arguments)

        try:
            return argument['rawText']
        except KeyError:
            return argument['textValue']

    @staticmethod
    def _is_health_check(arguments):
        try:
            health_check_argument = arguments['is_health_check']
        except KeyError:
            return False
        return health_check_argument['boolValue']
