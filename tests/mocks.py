import json


class MockRequest(object):
    def __init__(self, body=None, text=None, user_id=None, conversation_id=None):
        if body and (text or user_id or conversation_id):
            raise ValueError('If body is set you may not set any other paramaters.')
        self._body = body

        if not self._body:
            if text is None:
                text = 'TEXT_VALUE'
            if user_id is None:
                user_id = 'USER_ID'
            if conversation_id is None:
                conversation_id = 'CONVERSATION_ID'

            self._body = json.dumps({
                'user': {'userId': user_id},
                'conversation': {'conversationId': conversation_id},
                'inputs': [{'arguments': [{'textValue': text}]}],
            })

    @property
    def body(self):
        # Encode as utf-8 here, in case _body has intentially been set to a none utf-8 value to
        # throw an exception.
        return self._body.encode('utf-8')
