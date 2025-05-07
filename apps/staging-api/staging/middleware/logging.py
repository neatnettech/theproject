from starlette.middleware.base import BaseHTTPMiddleware
from structlog.contextvars import bind_contextvars, clear_contextvars
import structlog
import time


logger = structlog.get_logger()


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        clear_contextvars()

        bind_contextvars(
            method=request.method,
            path=request.url.path,
            ip=request.client.host,
        )

        if hasattr(request.state, "user_id"):
            bind_contextvars(user_id=request.state.user_id)

        start_time = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start_time

        bind_contextvars(status_code=response.status_code, duration=duration)
        logger.info("Request finished")

        return response