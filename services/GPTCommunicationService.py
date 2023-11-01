import json
import os
import openai
from dotenv import load_dotenv
import asyncio

class GPTCommunicationService:

    @staticmethod
    def send_message_to_gpt(message: str, system_instruction: str) -> dict:
        #Using openai api to communicate with gpt-3.5-turbo
        openai.api_key:str = os.getenv('OPENAI_API_KEY')
        response:dict = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": message}
            ]
        )
        return json.loads(response["choices"][0]["message"]["content"])