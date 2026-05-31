from opentelemetry import trace

from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter
)

from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider

from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor
)

from opentelemetry.instrumentation.fastapi import (
    FastAPIInstrumentor
)

from opentelemetry.instrumentation.psycopg2 import (
    Psycopg2Instrumentor
)


resource = Resource.create({
    "service.name": "auth-service"
})


trace.set_tracer_provider(
    TracerProvider(resource=resource)
)

tracer_provider = trace.get_tracer_provider()


otlp_exporter = OTLPSpanExporter(
    endpoint="http://jaeger:4318/v1/traces"
)


span_processor = BatchSpanProcessor(
    otlp_exporter
)

tracer_provider.add_span_processor(
    span_processor
)


def setup_telemetry(app):
    FastAPIInstrumentor.instrument_app(app)

    Psycopg2Instrumentor().instrument()
