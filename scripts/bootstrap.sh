#!/usr/bin/env bash
set -euo pipefail
./scripts/create-cluster.sh
./scripts/build-images.sh
./scripts/install-platform.sh
./scripts/deploy-app.sh
kubectl rollout status deployment/auth-service -n aiops --timeout=180s
kubectl rollout status deployment/catalog-service -n aiops --timeout=180s
kubectl rollout status deployment/order-service -n aiops --timeout=180s
kubectl rollout status deployment/ai-engine -n aiops --timeout=180s
./scripts/add-hosts.sh
./scripts/verify.sh
