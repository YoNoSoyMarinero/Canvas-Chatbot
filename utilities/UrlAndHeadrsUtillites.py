import os

class UrlAndHeadUtillites:
    @classmethod
    def create_headers(cls, token: str):
        return {"Authorization": f"Bearer {token}"}
    @classmethod
    def create_url(cls, path: str):
        return os.getenv('CANVAS_API_HOST') + path