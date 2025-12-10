import re


def clean_url(url: str) -> str:
    url = re.sub(r"^(https?://)?(www\.)?", "", url)
    return url.rstrip("/")


class FakeAiohttpResponse:
    def __init__(self, status=200):
        self.status = status

    async def read(self):
        return b""


class FakeAiohttpContextManager:
    def __init__(self, response: FakeAiohttpResponse):
        self.response = response

    async def __aenter__(self):
        return self.response

    async def __aexit__(self, exc_type, exc, tb):
        return False


class FakeAiohttpSession:
    def __init__(self, status=200):
        self.response = FakeAiohttpResponse(status=status)

    def get(self, url: str):
        # aiohttp.ClientSession.get MUST return an async context manager
        return FakeAiohttpContextManager(self.response)
