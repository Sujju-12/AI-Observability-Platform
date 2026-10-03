#!/usr/bin/env bash
set -euo pipefail
echo "=== Nodes ==="
kubectl get nodes -o wide
echo "=== Application Pods ==="
kubectl get pods -n aiops -o wide
echo "=== Services ==="
kubectl get svc -n aiops
echo "=== Ingress ==="
kubectl get ingress -n aiops
echo "=== Observability ==="
kubectl get pods -n aiops-observability
