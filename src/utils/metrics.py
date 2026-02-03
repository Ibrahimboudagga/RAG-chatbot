from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, FastAPI, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time


REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP Request Latency",
    ["method", "endpoint", "status_code"]
)

REQUEST_COUNT = Counter(
    "http_requests_total",
    "HTTP Request Count",
    ["method", "endpoint", "status_code"]
)


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=response.status_code
        ).observe(process_time)
        
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=response.status_code
        ).inc()

        return response

def setup_metrics(app: FastAPI):
    app.add_middleware(MetricsMiddleware)

    @app.get("/get_msg123çà", include_in_schema=False)
    async def metrics():
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)