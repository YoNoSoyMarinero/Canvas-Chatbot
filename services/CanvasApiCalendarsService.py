import os
import httpx
from utilities.HttpRequestUtillity import HttpRequestUtillity
from utilities.UrlAndHeadrsUtillites import UrlAndHeadUtillites
from fuzzywuzzy import fuzz
class CanvasApiCalendarServices:

    @classmethod
    async def get_calendar_events(cls, token:str) -> list:
        headers: dict = UrlAndHeadUtillites.create_headers(token)
        url: str = UrlAndHeadUtillites.create_url(f"/users/self/upcoming_events")
        res: httpx.Response = await HttpRequestUtillity.send_request("GET", url=url, headers=headers)

        return res.json()

    @staticmethod
    async def get_calendar_event_id_by_title(title: str, token: str) -> int:
        calendar_events: list = await CanvasApiCalendarServices.get_calendar_events(token)
        for calendar_event in calendar_events:
            if fuzz.ratio(calendar_event['title'], title) >= 80:
                return calendar_event['id']
        return -1
