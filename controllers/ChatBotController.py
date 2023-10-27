from schemas.UserMessageSchema import UserMessage
from services.GPTCommunicationService import GPTCommunicationService

class ChatBotController:
    @staticmethod
    def send_message_to_chatbot(user_message: UserMessage) -> dict:
        #Using service to provide response
        return GPTCommunicationService.send_message_to_gpt(user_message.message_text)
