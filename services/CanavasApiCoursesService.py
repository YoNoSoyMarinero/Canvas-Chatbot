import os

import httpx
import asyncio
from fuzzywuzzy import fuzz

from utilities.UrlAndHeadrsUtillites import UrlAndHeadUtillites
from utilities.HttpRequestUtillity import HttpRequestUtillity

class CanvasApiCoursesService:
    async def get_all_courses(self) -> list:
        headers: dict = UrlAndHeadUtillites.create_headers(os.getenv("CANVAS_ADMIN_KEY"))
        url: str = UrlAndHeadUtillites.create_url(f"/accounts/1/courses")
        res: httpx.Response = await HttpRequestUtillity.send_request("GET", url=url, headers=headers)

        return res.json()

    async def get_course_id_by_name(self, name: str) -> int:
        all_courses: list = await self.get_all_courses()
        for course in all_courses:
            if fuzz.ratio(course["name"], name) >= 70:
                return course["id"]

        return -1