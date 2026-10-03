#!/usr/bin/env bash
set -euo pipefail
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
helm repo update
helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace --set controller.service.type=NodePort
helm upgrade --install prometheus prometheus-community/prometheus --namespace aiops-observability --create-namespace
helm upgrade --install loki grafana/loki --namespace aiops-observability --set deploymentMode=SingleBinary --set loki.auth_enabled=false --set singleBinary.replicas=1
helm upgrade --install promtail grafana/promtail --namespace aiops-observability
helm upgrade --install jaeger jaegertracing/jaeger --namespace aiops-observability --set provisionDataStore.cassandra=false --set storage.type=memory
