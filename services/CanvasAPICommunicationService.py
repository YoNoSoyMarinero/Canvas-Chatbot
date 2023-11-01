import json

import httpx
import os
from schemas.UserMessageSchema import UserMessage
from services.GPTCommunicationService import GPTCommunicationService
from services.PromptBuilderService import PromptBuilderService
class CanvasApiCommunicatioService:

    @staticmethod
    def __canvas_create_course(user_message: UserMessage) -> dict:
        pass

    @staticmethod
    def __canvas_create_calendar_event(user_message: UserMessage) -> dict:
        pass

    @staticmethod
    def __canvas_create_enrollment(user_message: UserMessage) -> dict:
        pass

    @staticmethod
    def __canvas_create_user(user_message: UserMessage) -> dict:
        pass

    @staticmethod
    def __canvas_delete_calendar_event(user_message: UserMessage) -> dict:
        pass

    @staticmethod
    async def __canvas_get_students_on_course(user_message: UserMessage) -> dict:
        async with httpx.AsyncClient() as client:
            headers: dict = {"Authorization": f"Bearer {user_message.token}"}
            url: str = os.getenv('CANVAS_API_HOST') + f"/courses/{3}/students"
            res = await client.get(url, headers=headers, timeout=httpx.Timeout(timeout=10.0))
            if res.status_code == 200:
                server_response_data: dict = res.json()
                readable_response: dict = GPTCommunicationService.send_message_to_gpt(json.dumps(server_response_data),PromptBuilderService.system_instructions_human_readable_response())
                return readable_response
            else:
                return {"error-message": "Something went wrong"}

    @staticmethod
    async def __canvas_get_people_on_course(user_message: UserMessage) -> dict:
        async with httpx.AsyncClient() as client:
            headers: dict = {"Authorization": f"Bearer {user_message.token}"}
            url: str = os.getenv('CANVAS_API_HOST') + f"/courses/{3}/users"
            res = await client.get(url, headers=headers, timeout=httpx.Timeout(timeout=10.0))
            if res.status_code == 200:
                server_response_data: dict = res.json()
                readable_response: dict = GPTCommunicationService.send_message_to_gpt(json.dumps(server_response_data),PromptBuilderService.system_instructions_human_readable_response())
                return readable_response
            else:
                return {"error-message": "Something went wrong"}

    @staticmethod
    async def __canvas_get_courses_of_student(user_message: UserMessage) -> dict:
        async with httpx.AsyncClient() as client:
            headers: dict = {"Authorization": f"Bearer {user_message.token}"}
            url: str = os.getenv('CANVAS_API_HOST') + f"/users/{user_message.user_id}/courses"
            res = await client.get(url, headers=headers, timeout=httpx.Timeout(timeout=10.0))
            if res.status_code == 200:
                server_response_data: dict = res.json()
                readable_response: dict = GPTCommunicationService.send_message_to_gpt(json.dumps(server_response_data),PromptBuilderService.system_instructions_human_readable_response())
                return readable_response
            else:
                return {"error-message": "Something went wrong"}

    @staticmethod
    async def __canvas_get_all_upcoming_events(user_message: UserMessage) -> dict:
        async with httpx.AsyncClient() as client:
            headers: dict = {"Authorization": f"Bearer {user_message.token}"}
            url: str = os.getenv('CANVAS_API_HOST') + f"/users/self/upcoming_events"
            res = await client.get(url, headers=headers, timeout=httpx.Timeout(timeout=10.0))
            if res.status_code == 200:
                server_response_data: dict = res.json()
                readable_response: dict = GPTCommunicationService.send_message_to_gpt(json.dumps(server_response_data),PromptBuilderService.system_instructions_human_readable_response())
                return readable_response
            else:
                return {"error-message": "Something went wrong"}

    @staticmethod
    def __canvas_get_list_course_enrollments(user_message: UserMessage) -> dict:
        pass
    @staticmethod
    def __canvas_update_calendar_event(user_message: UserMessage) -> dict:
        pass

    @staticmethod
    def __default_action(user_message: UserMessage) -> dict:
        return {"message": "You should be more specific!"}

    __action_map: dict = {
        "action_create_new_course": __canvas_create_course,
        "action_create_new_calendar_event": __canvas_create_calendar_event,
        "action_create_new_enrollment_for_user": __canvas_create_enrollment,
        "action_create_new_user": __canvas_create_user,
        "action_delete_calendar_event": __canvas_delete_calendar_event,
        "action_list_of_all_students_which_attend_specific_courses": __canvas_get_students_on_course,
        "action_list_of_all_people_which_attend_specific_courses": __canvas_get_people_on_course,
        "action_list_of_all_courses_for_current_user_role_student": __canvas_get_courses_of_student,
        "action_list_of_all_upcoming_events": __canvas_get_all_upcoming_events,
        "action_list_course_enrollments": __canvas_get_list_course_enrollments,
        "action_update_calendar_event": __canvas_update_calendar_event,
        "action_not_specific_enough_to_figure_out_action": __default_action
    }

    @classmethod
    async def call_canvas_api_action(cls, action:str, user_message: UserMessage) -> dict:
        action: classmethod =  cls.__action_map.get(action)
        return await action(user_message)

