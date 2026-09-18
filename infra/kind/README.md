# Local Kind Cluster

DreamOps runs locally on Ubuntu/WSL2 using a single-node Kind cluster.

## Create

    kind create cluster --config infra/kind/cluster.yaml

## Verify

    kubectl cluster-info
    kubectl get nodes -o wide
    kubectl get pods -A

The host NGINX layer remains outside Kubernetes. Kubernetes ingress will be introduced after the cluster and test workload are healthy.
