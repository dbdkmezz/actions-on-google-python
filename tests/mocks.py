import json


class MockRequest(object):
    def __init__(self, body=None, argument_text_value=None):
        if body and argument_text_value:
            raise ValueError
        self._body = body
        self.argument_text_value = argument_text_value

    @property
    def body(self):
        if self._body:
            return self._body.encode('utf-8')

        if not self.argument_text_value:
            input_dict = {}
        else:
            input_dict = {'arguments': [{'textValue': self.argument_text_value}]}
        return json.dumps({
            'user': {'userId': 'TEST_USER_ID'},
            'conversation': {'conversationId': 'TEST_CONVERSATION_ID'},
            'inputs': [input_dict],
        }).encode('utf-8')
