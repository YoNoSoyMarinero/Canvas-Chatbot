from schemas.UserMessageSchema import UserMessage
from services.GPTCommunicationService import GPTCommunicationService
from services.MessagePreprocessingService import MessagePreprocessingPipelineService

class ChatBotController:
    @staticmethod
    def send_message_to_chatbot(user_message: UserMessage) -> dict:
        user_message_text_preprocessed: str = MessagePreprocessingPipelineService.preprocess_message_pipeline(user_message.message_text)
        return GPTCommunicationService.send_message_to_gpt(user_message.message_text)
