#!/usr/bin/env bash
set -euo pipefail
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana-community https://grafana-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

kubectl create namespace aiops-observability --dry-run=client -o yaml | kubectl apply -f -

helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace --set controller.service.type=NodePort
helm upgrade --install prometheus prometheus-community/prometheus --namespace aiops-observability
helm upgrade --install grafana grafana-community/grafana --namespace aiops-observability -f infra/observability/grafana-values.yaml
helm upgrade --install loki grafana-community/loki --namespace aiops-observability -f infra/observability/loki-values.yaml
helm upgrade --install alloy grafana/alloy --namespace aiops-observability --set controller.type=daemonset --set-file alloy.configMap.content=infra/observability/alloy.alloy

kubectl apply -f infra/observability/jaeger-config.yaml
kubectl apply -f infra/observability/jaeger.yaml
