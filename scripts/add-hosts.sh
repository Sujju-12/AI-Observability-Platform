#!/usr/bin/env bash
set -euo pipefail
HOSTS_LINE="127.0.0.1 api.aiops.test grafana.aiops.test jaeger.aiops.test prometheus.aiops.test"
if ! grep -q "api.aiops.test" /etc/hosts; then
  echo "$HOSTS_LINE" | sudo tee -a /etc/hosts
else
  echo "aiops host aliases already present"
fi
