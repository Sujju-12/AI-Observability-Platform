# DreamOps Local Architecture

## Objective

Build and operate an AI-assisted Kubernetes troubleshooting platform on local Ubuntu/WSL2 without EKS or EC2.

## Traffic path

    Client
      |
      v
    Host NGINX :80
      |
      v
    Kind port mapping :8080
      |
      v
    Kubernetes Ingress
      |
      v
    Service
      |
      v
    Pod

## Control and intelligence path

    Kubernetes
       |
       +--> metrics/logs/traces
       |
       v
    DreamOps collector
       |
       v
    Diagnosis + trajectory store
       |
       v
    Ollama / Qwen
       |
       v
    RCA + remediation recommendation

## Resource strategy

The local environment has limited memory, so components are introduced incrementally. The first milestone is only Kind + a tiny NGINX workload. Observability and the AI layer come later.

## Safety boundary

The troubleshooting agent should initially be read-only. Remediation becomes an explicit, versioned workflow with validation and approval gates rather than allowing an agent to mutate production state arbitrarily.
