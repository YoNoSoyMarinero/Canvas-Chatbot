import requests
import os
from schemas.UserMessageSchema import UserMessage

class CanvasApiCommunicatioService:

    @classmethod
    def call_canvas_api_action(cls, action:str, user_message: UserMessage) -> dict:
        print(action)
        if action == "create_course":
            return cls.__canvas_create_course()
        elif action == "create_calendar_event":
            return cls.__canvas_create_calendar_event()
        elif action == "create_enrollment":
            return cls.__canvas_create_enrollment()
        elif action == "create_user":
            return cls.__canvas_create_user()
        elif action == "delete_calendar_event":
            return cls.__canvas_delete_calendar_event()
        elif action == "list_students_on_course":
            return cls.__canvas_get_students_on_course(user_message)
        elif action == "list_people_on_course":
            return cls.__canvas_get_people_on_course()
        elif action == "list_courses_of_student":
            return cls.__canvas_get_courses_of_student(user_message)
        elif action == "list_user_to_do_tasks":
            return cls.__canvas_get_to_do_tasks()
        elif action == "list_course_enrollments":
            return cls.__canvas_get_list_course_enrollments()
        elif action == "update_calendar_event":
            return cls.__canvas_update_calendar_event()
        else:
            return {"error-message": "Something went wrong"}
    @classmethod
    def __canvas_create_course(cls) -> dict:
        pass

    @classmethod
    def __canvas_create_calendar_event(cls) -> dict:
        pass

    @classmethod
    def __canvas_create_enrollment(cls) -> dict:
        pass

    @classmethod
    def __canvas_create_user(cls) -> dict:
        pass

    @classmethod
    def __canvas_delete_calendar_event(cls) -> dict:
        pass

    @classmethod
    def __canvas_get_students_on_course(cls, user_message) -> dict:
        headers: dict = {"Authorization": f"Bearer {user_message.token}"}
        url: str = os.getenv('CANVAS_API_HOST') + f"/courses/{3}/students"
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.json()
        else:
            return {"error-message": "Something went wrong"}
    @classmethod
    def __canvas_get_people_on_course(cls) -> dict:
        pass

    @classmethod
    def __canvas_get_courses_of_student(cls, user_message: UserMessage) -> dict:
        headers: dict = {"Authorization": f"Bearer {user_message.token}"}
        url: str = os.getenv('CANVAS_API_HOST') + f"/user/{user_message.user_id}/courses"
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.json()
        else:
            return {"error-message": "Something went wrong"}

    @classmethod
    def __canvas_get_to_do_tasks(cls) -> dict:
        pass

    @classmethod
    def __canvas_get_list_course_enrollments(cls) -> dict:
        pass

    @classmethod
    def __canvas_update_calendar_event(cls) -> dict:
        pass
