# Enterprise Local Architecture

The platform models a production-style Kubernetes request and incident path.

Client -> DNS -> NGINX Ingress -> Kubernetes Service -> application replicas -> dependencies.

Application:
- auth-service
- catalog-service
- order-service
- PostgreSQL

Observability:
- Prometheus
- Grafana
- Loki
- OpenTelemetry
- Jaeger

AI:
- Kubernetes state and events are collected as evidence.
- Prometheus metrics are queried as evidence.
- Deterministic signatures provide a safe baseline RCA.
- Optional local Ollama provides LLM reasoning over the evidence.
- RAG is intentionally not required until real runbooks and incident reports exist.

Failure engineering:
- CrashLoopBackOff
- OOMKilled
- ImagePullBackOff
- Pending / scheduling failure
