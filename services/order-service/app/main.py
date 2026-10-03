import os, uuid
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from prometheus_fastapi_instrumentator import Instrumentator

VERSION = os.getenv("APP_VERSION","1.0.0")
AUTH_URL = os.getenv("AUTH_SERVICE_URL","http://auth-service:8000")
CATALOG_URL = os.getenv("CATALOG_SERVICE_URL","http://catalog-service:8001")
app = FastAPI(title="Order Service", version=VERSION)
provider = TracerProvider(resource=Resource.create({"service.name":"order-service","service.version":VERSION}))
provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT","http://jaeger-collector:4318/v1/traces"))))
trace.set_tracer_provider(provider)
FastAPIInstrumentor.instrument_app(app)
HTTPXClientInstrumentor().instrument()
Instrumentator().instrument(app).expose(app)

class Order(BaseModel):
    user_id: str
    product_id: str
    quantity: int = 1

@app.get("/")
def root():
    return {"service":"order-service","version":VERSION}

@app.get("/health")
def health():
    return {"status":"healthy","service":"order-service","version":VERSION}

@app.post("/orders")
async def create_order(order: Order):
    async with httpx.AsyncClient(timeout=3) as client:
        auth = await client.get(f"{AUTH_URL}/health")
        if auth.status_code != 200:
            raise HTTPException(status_code=503, detail="auth dependency unavailable")
        product = await client.get(f"{CATALOG_URL}/products/{order.product_id}")
        if product.status_code != 200:
            raise HTTPException(status_code=404, detail="product unavailable")
    return {"order_id":str(uuid.uuid4()),"status":"created","user_id":order.user_id,"product_id":order.product_id,"quantity":order.quantity,"version":VERSION}
