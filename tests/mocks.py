import json


class MockRequest(object):
    def __init__(self, body=None, text=None, user_id=None, conversation_token=None,
                 conversation_id=None, health_check=False):
        if body and (text or user_id or conversation_token or conversation_id):
            raise ValueError('If body is set you may not set any other paramaters.')
        self._body = body

        if not self._body:
            if text is None:
                text = 'TEXT_VALUE'
            if user_id is None:
                user_id = 'USER_ID'
            if conversation_id is None:
                conversation_id = 'CONVERSATION_ID'

            arguments = []
            if text:
                arguments.append({'name': 'text', 'textValue': text, 'rawText': text})
            if health_check:
                arguments.append({'name': 'is_health_check', 'textValue': '1', 'boolValue': True})

            self._body = json.dumps({
                'user': {'userId': user_id},
                'conversation': {
                    'conversationId': conversation_id,
                    'conversationToken': conversation_token,
                },
                'inputs': [{'arguments': arguments}],
            })

    @property
    def body(self):
        # Encode as utf-8 here, in case _body has intentially been set to a none utf-8 value to
        # throw an exception.
        return self._body.encode('utf-8')
