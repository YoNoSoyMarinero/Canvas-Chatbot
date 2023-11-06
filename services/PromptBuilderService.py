import json

class PromptBuilderService:


    with open('json_prompt_files/getting_action_prompt_template.json') as f:
        __action_propmt_template: dict = json.load(f)

    with open('json_prompt_files/getting_human_readable_message.json') as f:
        __human_readable_response: dict = json.load(f)

    with open('json_prompt_files/getting_course_name_from_promt.json') as f:
        __course_name: dict = json.load(f)

    with open('json_prompt_files/system_instruction_json_template.json') as f:
        __instruction_json_template: dict = json.load(f)

    @classmethod
    def system_insturction_course_name(cls) -> str:
        return cls.__course_name['system_instructions']
    @classmethod
    def system_instructions_actions(cls) -> str:
        return cls.__action_propmt_template['system_instructions']

    @classmethod
    def message_instruction_human_readable_response(cls, instruction: str) -> str:
        return cls.__human_readable_response[instruction]

    @classmethod
    def system_instructions_human_readable_response(cls) -> str:
        return cls.__human_readable_response['system_instructions']
    @classmethod
    def system_instruction_create_user(cls) -> str:
        return cls.__instruction_json_template['system_instructions_create_user']

    @classmethod
    def system_instruction_create_calendar_event(cls) -> str:
        return cls.__instruction_json_template['system_instructions_create_calendar_event']

    @classmethod
    def system_instruction_create_enrollment(cls) -> str:
        return cls.__instruction_json_template['system_instructions_create_enrollment']

    @classmethod
    def system_instruction_create_course(cls) -> str:
        return cls.__instruction_json_template['system_instructions_create_course']
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

