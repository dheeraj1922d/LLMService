from utils.messageUtils import messageUtils
from service.llmService import LLMService

class MessageService:
    def __init__(self):
        self.messageUtils = messageUtils()
        self.llmService = LLMService()

    def process_message(self, message):
        print(type(message))
        if self.messageUtils.isBankSMS(message):
            return self.llmService.runLLM(message)
        else:
            return None