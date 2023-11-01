import json

class PromptBuilderService:


    with open('json_prompt_files/getting_action_prompt_template.json') as f:
        __action_propmt_template: dict = json.load(f)

    with open('json_prompt_files/getting_human_readable_message.json') as f:
        __human_readable_response: dict = json.load(f)

    @classmethod
    def system_instructions_actions(cls) -> str:
        return cls.__action_propmt_template['system_instructions']

    @classmethod
    def system_instructions_human_readable_response(cls) -> str:
        return cls.__human_readable_response['system_instructions']
    @classmethod
    def create_message_prompt_to_choose_action(cls, message: str) -> str:
        message_actions: list = cls.__action_propmt_template['message_actions']['message_action']
        message_actions_prompts: str = " ".join(message_actions)
        #reading parts of message that defeins prompt for gpt
        message: str = f"{cls.__action_propmt_template['message_header']} " \
               f"{message} " \
               f"{cls.__action_propmt_template['message_task']} " \
               f"{message_actions_prompts} " \

        return message

