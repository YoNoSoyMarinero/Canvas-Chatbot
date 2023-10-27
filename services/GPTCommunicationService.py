import os
import openai
from dotenv import load_dotenv

class GPTCommunicationService:

    @staticmethod
    def send_message_to_gpt(message: str) -> dict:
        #Using openai api to communicate with gpt-3.5-turbo
        openai.api_key = os.getenv('OPENAI_API_KEY')
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message}
            ]
        )
        return response