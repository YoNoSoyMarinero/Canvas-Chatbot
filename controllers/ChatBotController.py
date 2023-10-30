from schemas.UserMessageSchema import UserMessage
from services.GPTCommunicationService import GPTCommunicationService
from services.MessagePreprocessingService import MessagePreprocessingPipelineService
from services.PromptBuilderService import PromptBuilderService

class ChatBotController:
    @staticmethod
    def send_message_to_chatbot(user_message: UserMessage) -> dict:
        user_message_text_preprocessed: str = MessagePreprocessingPipelineService.preprocess_message_pipeline(user_message.message_text)
        action_decision_prompt: str = PromptBuilderService.create_message_prompt_to_choose_action(user_message_text_preprocessed)
        system_instruction: str = PromptBuilderService.system_instuctions()
        canvas_action: dict = GPTCommunicationService.send_message_to_gpt(action_decision_prompt, system_instruction)
        return canvas_action
