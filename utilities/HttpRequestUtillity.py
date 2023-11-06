import httpx

class HttpRequestUtillity:

    @staticmethod
    async def send_request(method: str, headers: dict, url: str, body:dict=None):
        async with httpx.AsyncClient() as client:
            if method == "POST":
                res = await client.post(url, headers=headers, json=body, timeout=httpx.Timeout(timeout=10.0))
            elif method == "PUT":
                res = await client.put(url, headers=headers, json=body, timeout=httpx.Timeout(timeout=10.0))
            elif method == "DELETE":
                res = await client.delete(url, headers=headers, timeout=httpx.Timeout(timeout=10.0))
            elif method == "GET":
                res = await client.get(url, headers= headers, timeout=httpx.Timeout(timeout=10.0))
        return res