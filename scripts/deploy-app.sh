#!/usr/bin/env bash
set -euo pipefail
kubectl apply -f k8s/base/namespace.yaml
kubectl apply -f k8s/base/postgres/
kubectl apply -f k8s/base/auth-service/
kubectl apply -f k8s/apps/auth-patch.yaml
kubectl apply -f k8s/apps/catalog.yaml
kubectl apply -f k8s/apps/order.yaml
kubectl apply -f k8s/cluster/rbac-ai-engine.yaml
kubectl apply -f k8s/apps/ai-engine.yaml
kubectl apply -f k8s/cluster/ingress.yaml
