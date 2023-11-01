from schemas.UserMessageSchema import UserMessage
from services.GPTCommunicationService import GPTCommunicationService
from services.MessagePreprocessingService import MessagePreprocessingPipelineService
from services.PromptBuilderService import PromptBuilderService
from services.CanvasAPICommunicationService import CanvasApiCommunicatioService
import asyncio
class ChatBotController:
    @classmethod
    async def send_message_to_chatbot(cls, user_message: UserMessage) -> dict:
        user_message_text_preprocessed: str = MessagePreprocessingPipelineService.preprocess_message_pipeline(user_message.message_text)
        action_decision_prompt: str = PromptBuilderService.create_message_prompt_to_choose_action(user_message_text_preprocessed)
        system_instruction: str = PromptBuilderService.system_instructions_actions()
        canvas_action: dict = GPTCommunicationService.send_message_to_gpt(action_decision_prompt, system_instruction)
        res: dict = await CanvasApiCommunicatioService.call_canvas_api_action(action=canvas_action['message_action'], user_message=user_message)
        return res
