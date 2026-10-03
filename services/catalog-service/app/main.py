import os
from fastapi import FastAPI, HTTPException
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from prometheus_fastapi_instrumentator import Instrumentator

VERSION = os.getenv("APP_VERSION", "1.0.0")
app = FastAPI(title="Catalog Service", version=VERSION)
provider = TracerProvider(resource=Resource.create({"service.name":"catalog-service","service.version":VERSION}))
provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT","http://jaeger-collector:4318/v1/traces"))))
trace.set_tracer_provider(provider)
FastAPIInstrumentor.instrument_app(app)
Instrumentator().instrument(app).expose(app)

PRODUCTS = {
    "p100": {"id":"p100","name":"Laptop","price":799.0,"stock":25},
    "p200": {"id":"p200","name":"Keyboard","price":49.0,"stock":100},
    "p300": {"id":"p300","name":"Monitor","price":249.0,"stock":40}
}

@app.get("/")
def root():
    return {"service":"catalog-service","version":VERSION}

@app.get("/health")
def health():
    return {"status":"healthy","service":"catalog-service","version":VERSION}

@app.get("/products")
def products():
    return list(PRODUCTS.values())

@app.get("/products/{product_id}")
def product(product_id: str):
    item = PRODUCTS.get(product_id)
    if not item:
        raise HTTPException(status_code=404, detail="product not found")
    return item

@app.get("/products/{product_id}/availability")
def availability(product_id: str):
    item = PRODUCTS.get(product_id)
    if not item:
        raise HTTPException(status_code=404, detail="product not found")
    return {"product_id":product_id,"available":item["stock"] > 0,"stock":item["stock"]}
