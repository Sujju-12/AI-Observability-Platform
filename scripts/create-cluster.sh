#!/usr/bin/env bash
set -euo pipefail
kind create cluster --config kind/aiops-kind.yaml
kubectl apply -f k8s/cluster/namespace.yaml
