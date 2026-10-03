#!/usr/bin/env bash
set -euo pipefail
docker build -t auth-service:v0.1.2 services/auth-service
docker build -t catalog-service:v1.0.0 services/catalog-service
docker build -t order-service:v1.0.0 services/order-service
docker build -t ai-engine:v1.0.0 services/ai-engine
for image in auth-service:v0.1.2 catalog-service:v1.0.0 order-service:v1.0.0 ai-engine:v1.0.0; do
  kind load docker-image "$image" --name aiops-local
done
