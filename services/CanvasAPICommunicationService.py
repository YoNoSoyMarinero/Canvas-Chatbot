import json
import re
import httpx
import os
from schemas.UserMessageSchema import UserMessage
from services.GPTCommunicationService import GPTCommunicationService
from services.PromptBuilderService import PromptBuilderService
from services.CanavasApiCoursesService import CanvasApiCoursesService
from services.CanvasApiUsersService import CanvasApiUsersService
from utilities.UrlAndHeadrsUtillites import UrlAndHeadUtillites
from utilities.HttpRequestUtillity import HttpRequestUtillity
class CanvasApiCommunicatioService:

    @classmethod
    async def __canvas_send_request(cls,method:str, path: str, token: str = None,body:dict = None) -> httpx.Response:
        url: str = UrlAndHeadUtillites.create_url(path)
        token:str = token if token else os.getenv(("CANVAS_ADMIN_KEY"))
        headers: dict = UrlAndHeadUtillites.create_headers(token)
        return await HttpRequestUtillity.send_request(method=method, url=url, headers=headers, body=body)
    @classmethod
    def __canvas_handle_response(cls, res: httpx.Response, insturction: str):
        response_message: dict = res.json()
        system_instruction: str =PromptBuilderService.system_instructions_human_readable_response() +\
                             PromptBuilderService.message_instruction_human_readable_response(insturction)
        readable_response: dict = GPTCommunicationService\
            .send_message_to_gpt(
            json.dumps(response_message),
            system_instruction
            )
        readable_response['status'] = res.status_code
        return readable_response

    @staticmethod
    async def __canvas_create_course(user_message: UserMessage) -> dict:
        course_json: dict = GPTCommunicationService.send_message_to_gpt(user_message.message_text,
                                                                     PromptBuilderService
                                                                     .system_instruction_create_course())
        course_json['course']['event'] = "offer"
        course_json['course']['offer'] = True
        course_json['offer'] = True
        res: httpx.Response = await CanvasApiCommunicatioService.__canvas_send_request(
            method="POST",
            path="/accounts/1/courses",
            body=course_json)
        return CanvasApiCommunicatioService.__canvas_handle_response(res, "element_created")

    @staticmethod
    async def __canvas_create_calendar_event(user_message: UserMessage) -> dict:
        canvas_api_user_service: CanvasApiUsersService = CanvasApiUsersService()
        user_id: int = await canvas_api_user_service.get_user_id_by_login_id(user_message.user_email)
        context_code: str = "user_" + str(user_id)
        calendar_event_json: dict = GPTCommunicationService.send_message_to_gpt(user_message.message_text,
                                                                     PromptBuilderService
                                                                     .system_instruction_create_calendar_event())
        calendar_event_json['calendar_event']['context_code'] = context_code
        calendar_event_json['calendar_event']['all_day'] = False
        res: httpx.Response = await CanvasApiCommunicatioService.__canvas_send_request(
            method="POST",
            path="/calendar_events",
            token=user_message.token,
            body=calendar_event_json)
        return CanvasApiCommunicatioService.__canvas_handle_response(res, "element_created")

    @staticmethod
    async def __canvas_create_enrollment(user_message: UserMessage) -> dict:
        canvas_api_courses_service: CanvasApiCoursesService = CanvasApiCoursesService()
        course_name: dict = GPTCommunicationService.send_message_to_gpt(user_message.message_text,
                                                                        PromptBuilderService
                                                                        .system_insturction_course_name())
        course_id: int = await canvas_api_courses_service.get_course_id_by_name(course_name['course_name'])
        if course_id == -1:
            return {"readable-message": "That course doesn't exist!", "status": 400}

        email_pattern: str = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        emails: list = re.findall(email_pattern, user_message.message_text)
        email: str = emails[0] if len(emails) > 0 else ""
        canvas_api_user_service: CanvasApiUsersService = CanvasApiUsersService()
        user_id: int = await canvas_api_user_service.get_user_id_by_login_id(email=email)
        if user_id == -1:
            return {"readable-message": "That user doesn't exist!", "status": 400}
        enrollment_gpt: dict = GPTCommunicationService.send_message_to_gpt(user_message.message_text,
                                                                     PromptBuilderService
                                                                     .system_instruction_create_enrollment())
        enrollment: dict = {'enrollment': {}}
        enrollment['enrollment']['type'] = enrollment_gpt['enrollment']['type']
        enrollment['enrollment']['user_id'] = user_id
        enrollment['enrollment']['notify'] = True
        enrollment['enrollment']['enrollment_state'] = "active"
        res: httpx.Response = await CanvasApiCommunicatioService.__canvas_send_request(
            method="POST",
            path=f"/courses/{course_id}/enrollments",
            body=enrollment)
        return CanvasApiCommunicatioService.__canvas_handle_response(res, "element_created")



    @staticmethod
    async def __canvas_create_user(user_message: UserMessage) -> dict:
        user_json: dict = GPTCommunicationService.send_message_to_gpt(user_message.message_text,
                                                                      PromptBuilderService.
                                                                      system_instruction_create_user())
        user_json['user']['time_zone'] = "America/New York"
        user_json['user']['locale'] = "en-US"
        user_json['user']['terms_of_use'] = True
        user_json['user']['skip_registration'] = False
        res: httpx.Response = await CanvasApiCommunicatioService.__canvas_send_request(
            method="POST",
            path="/accounts/1/users",
            body=user_json)
        return CanvasApiCommunicatioService.__canvas_handle_response(res, "element_created")
    @staticmethod
    def __canvas_delete_calendar_event(user_message: UserMessage) -> dict:
        pass

    @staticmethod
    async def __canvas_get_students_on_course(user_message: UserMessage) -> dict:
        canvas_api_courses_service: CanvasApiCoursesService = CanvasApiCoursesService()
        course_name: dict = GPTCommunicationService.send_message_to_gpt(user_message.message_text,
                                                                        PromptBuilderService
                                                                        .system_insturction_course_name())
        course_id: int = await canvas_api_courses_service.get_course_id_by_name(course_name['course_name'])
        if course_id == -1:
            return {"readable-message": "That course doesn't exist!", "status": 400}
        res: httpx.Response = await CanvasApiCommunicatioService.__canvas_send_request(
            method="GET",
            path=f"/courses/{course_id}/students",
            token= user_message.token)
        return CanvasApiCommunicatioService.__canvas_handle_response(res, "elements_listed")

    @staticmethod
    async def __canvas_get_people_on_course(user_message: UserMessage) -> dict:
        canvas_api_courses_service: CanvasApiCoursesService = CanvasApiCoursesService()
        course_name: dict = GPTCommunicationService.send_message_to_gpt(user_message.message_text, PromptBuilderService
                                                                        .system_insturction_course_name())

        course_id: int = await canvas_api_courses_service.get_course_id_by_name(course_name['course_name'])
        if course_id == -1:
            return {"readable-message": "That course doesn't exist!", "status": 400}
        res: httpx.Response = await CanvasApiCommunicatioService.__canvas_send_request(
            method="GET",
            path=f"/courses/{course_id}/users",
            token=user_message.token)
        return CanvasApiCommunicatioService.__canvas_handle_response(res, "elements_listed")

    @staticmethod
    async def __canvas_get_courses_of_student(user_message: UserMessage) -> dict:
        headers: dict = UrlAndHeadUtillites.create_headers(user_message.token)
        canvas_api_user_service: CanvasApiUsersService = CanvasApiUsersService()
        user_id: int = await canvas_api_user_service.get_user_id_by_login_id(user_message.user_email)
        if user_id == -1:
            return {"readable-message": "That user doesn't exist!", "status": 400}
        res: httpx.Response = await CanvasApiCommunicatioService.__canvas_send_request(
            method="GET",
            path=f"/users/{user_id}/courses",
            token=user_message.token)
        return CanvasApiCommunicatioService.__canvas_handle_response(res, "elements_listed")

    @staticmethod
    async def __canvas_get_all_upcoming_events(user_message: UserMessage) -> dict:
        res: httpx.Response = await CanvasApiCommunicatioService.__canvas_send_request(
            method="GET",
            path=f"/users/self/upcoming_events",
            token=user_message.token)
        return CanvasApiCommunicatioService.__canvas_handle_response(res, "elements_listed")

    @staticmethod
    def __canvas_update_calendar_event(user_message: UserMessage) -> dict:
        pass

    @staticmethod
    def __default_action(user_message: UserMessage) -> dict:
        return {"readable_message": "You should be more specific!"}

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
        "action_update_calendar_event": __canvas_update_calendar_event,
        "action_not_specific_enough_to_figure_out_action": __default_action
    }

    @classmethod
    async def call_canvas_api_action(cls, action:str, user_message: UserMessage) -> dict:
        action_method: classmethod =  cls.__action_map.get(action)
        return await action_method(user_message)

