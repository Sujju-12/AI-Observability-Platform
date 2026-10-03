from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
import os

resource = Resource.create({"service.name": "auth-service"})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer_provider = trace.get_tracer_provider()

otlp_exporter = OTLPSpanExporter(
    endpoint=os.getenv(
        "OTEL_EXPORTER_OTLP_ENDPOINT",
        "http://jaeger.aiops-observability.svc.cluster.local:4318/v1/traces",
    )
)
tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

def setup_telemetry(app):
    FastAPIInstrumentor.instrument_app(app)
    Psycopg2Instrumentor().instrument()
