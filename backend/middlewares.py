from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request, Response
from starlette.types import ASGIApp

from logging import Logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    def __init__(self, app: ASGIApp, logger: Logger):
        super().__init__(app)
        self.logger = logger

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        url = request.url.path
        self.logger.info(f"Request: {method} {url} from {client_ip}")

        response = await call_next(request)

        status_code = response.status_code
        self.logger.info(
            f"Response: {method} {url} returned {status_code} to {client_ip}"
        )
        return response
