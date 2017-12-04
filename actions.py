# https://developers.google.com/actions/reference/rest/Shared.Types/AppResponse

import logging


class GoogleActions(object):
    def __init__(self, logger=logging.getLogger(), sandbox=True):
        self.logger = logger
        self.sandbox = sandbox

    def ask(self, text, conversation_token=None):
        """Continues the conversation.

        text: the message to send back to the user
        conversation_token: a token which will be recycled by Google back to us in the next request.
           Can be used by an app to track the conversation or to store conversation related data.
        """

        self.logger.debug('Asking {}'.format(text))
        response = self._base_response(self.sandbox, conversation_token)
        response.update({
            'expectUserResponse': True,
            'expectedInputs': {
                'inputPrompt': {
                    'richInitialPrompt': {
                        'items': [self._generate_response_item(text)],
                    },
                },
                'possibleIntents': [
                    {
                        'intent': 'actions.intent.TEXT',
                    }
                ],
            }
        })
        return response

    def tell(self, text, conversation_token=None):
        """Ends the conversation

        text: the message to send back to the user
        conversation_token: a token which will be recycled by Google back to us in the next request.
           Can be used by an app to track the conversation or to store conversation related data.
        """

        self.logger.debug('Telling {}'.format(text))
        response = self._base_response(self.sandbox, conversation_token)
        response.update({
            'expectUserResponse': False,
            'isInSandbox': self.sandbox,
            'finalResponse': {
                'richResponse': {
                    'items': [self._generate_response_item(text)],
                }
            },
        })
        return response

    @staticmethod
    def _base_response(sandbox, conversation_token):
        response = {'isInSandbox': sandbox}
        if conversation_token:
            response['conversationToken'] = conversation_token
        return response

    @staticmethod
    def _generate_response_item(text):
        return {
            'simpleResponse': {
                'textToSpeech': text,
            }
        }
