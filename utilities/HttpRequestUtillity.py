import httpx

class HttpRequestUtillity:

    @staticmethod
    async def send_request(method: str, headers: dict, url: str, body:dict=None) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            if method == "POST":
                res: httpx.Response = await client.post(url, headers=headers, json=body, timeout=httpx.Timeout(timeout=10.0))
            elif method == "PUT":
                res: httpx.Response = await client.put(url, headers=headers, json=body, timeout=httpx.Timeout(timeout=10.0))
            elif method == "DELETE":
                res: httpx.Response = await client.delete(url, headers=headers, timeout=httpx.Timeout(timeout=10.0))
            elif method == "GET":
                res: httpx.Response = await client.get(url, headers= headers, timeout=httpx.Timeout(timeout=10.0))

        return res