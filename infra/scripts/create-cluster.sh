#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

command -v docker >/dev/null || { echo "Docker is required."; exit 1; }
command -v kind >/dev/null || { echo "Kind is required."; exit 1; }
command -v kubectl >/dev/null || { echo "kubectl is required."; exit 1; }

if kind get clusters | grep -qx "dreamops"; then
  echo "Kind cluster 'dreamops' already exists."
else
  kind create cluster --config infra/kind/cluster.yaml
fi

kubectl cluster-info
kubectl get nodes -o wide
