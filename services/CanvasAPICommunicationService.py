import requests
import os
from schemas.UserMessageSchema import UserMessage

class CanvasApiCommunicatioService:

    @staticmethod
    def __canvas_create_course() -> dict:
        pass

    @staticmethod
    def __canvas_create_calendar_event() -> dict:
        pass

    @staticmethod
    def __canvas_create_enrollment() -> dict:
        pass

    @staticmethod
    def __canvas_create_user() -> dict:
        pass

    @staticmethod
    def __canvas_delete_calendar_event() -> dict:
        pass

    @staticmethod
    def __canvas_get_students_on_course(user_message) -> dict:
        headers: dict = {"Authorization": f"Bearer {user_message.token}"}
        url: str = os.getenv('CANVAS_API_HOST') + f"/courses/{3}/students"
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.json()
        else:
            return {"error-message": "Something went wrong"}

    @staticmethod
    def __canvas_get_people_on_course() -> dict:
        pass

    @staticmethod
    def __canvas_get_courses_of_student(user_message: UserMessage) -> dict:
        headers: dict = {"Authorization": f"Bearer {user_message.token}"}
        url: str = os.getenv('CANVAS_API_HOST') + f"/user/{user_message.user_id}/courses"
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.json()
        else:
            return {"error-message": "Something went wrong"}

    @staticmethod
    def __canvas_get_to_do_tasks() -> dict:
        pass

    @staticmethod
    def __canvas_get_list_course_enrollments() -> dict:
        pass
    @staticmethod
    def __canvas_update_calendar_event() -> dict:
        pass

    __action_map: dict = {
        "create_course": __canvas_create_course,
        "create_calendar_event": __canvas_create_calendar_event,
        "create_enrollment": __canvas_create_enrollment,
        "create_user": __canvas_create_user,
        "delete_calendar_event": __canvas_delete_calendar_event,
        "list_students_on_course": __canvas_get_students_on_course,
        "list_people_on_course": __canvas_get_people_on_course,
        "list_courses_of_student": __canvas_get_courses_of_student,
        "list_user_to_do_tasks": __canvas_get_to_do_tasks,
        "list_course_enrollments": __canvas_get_list_course_enrollments,
        "update_calendar_event": __canvas_update_calendar_event,
    }

    @classmethod
    def call_canvas_api_action(cls, action:str, user_message: UserMessage) -> dict:
        action: classmethod = cls.__action_map.get(action)
        return action(user_message)

