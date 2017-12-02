import logging


class GoogleActions(object):
    def __init__(self, logger=logging.getLogger(), sandbox=True):
        self.logger = logger
        self.sandbox = sandbox

    def ask(self, text):
        self.logger.debug("Asking {}".format(text))
        return {
            "expectUserResponse": True,
            "isInSandbox": self.sandbox,
            "expectedInputs": {
                "inputPrompt": {
                    "richInitialPrompt": {
                        "items": [self._generate_response_item(text)],
                    },
                },
                "possibleIntents": [
                    {
                        'intent': "actions.intent.TEXT",
                    }
                ],
            }
        }

    def tell(self, text):
        """Ends the conversation"""
        self.logger.debug("Telling {}".format(text))
        return {
            "expectUserResponse": False,
            "isInSandbox": self.sandbox,
            "finalResponse": {
                "richResponse": {
                    "items": [self._generate_response_item(text)],
                }
            },
        }

    @staticmethod
    def _generate_response_item(text):
        return {
            "simpleResponse": {
                "textToSpeech": text,
            }
        }
