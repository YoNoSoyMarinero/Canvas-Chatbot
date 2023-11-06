import os
import httpx

from utilities.UrlAndHeadrsUtillites import UrlAndHeadUtillites

class CanvasApiUsersService:
    async def get_all_users(self) -> list:
        headers: dict = UrlAndHeadUtillites.create_headers(os.getenv("CANVAS_ADMIN_KEY"))
        url: str = UrlAndHeadUtillites.create_url(f"/accounts/1/users")
        async with httpx.AsyncClient() as client:
            res = await client.get(url, headers=headers, timeout=httpx.Timeout(timeout=10.0))

        return res.json()
    async def get_user_id_by_login_id(self, email: str) -> int:
        all_users: list = await self.get_all_users()
        for user in all_users:
            if user["login_id"] == email:
                return user["id"]

        return -1