#!/usr/bin/env bash
set -euo pipefail
case "${1:-}" in
  oom) kubectl apply -f k8s/failures/oomkill.yaml ;;
  crashloop) kubectl apply -f k8s/failures/crashloop.yaml ;;
  imagepull) kubectl apply -f k8s/failures/imagepullbackoff.yaml ;;
  pending) kubectl apply -f k8s/failures/pending.yaml ;;
  clean) kubectl delete deployment aiops-oom-test aiops-crash-test aiops-imagepull-test aiops-pending-test -n aiops --ignore-not-found ;;
  *) echo "Usage: $0 {oom|crashloop|imagepull|pending|clean}"; exit 1 ;;
esac
