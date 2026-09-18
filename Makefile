SHELL := /bin/bash

.PHONY: cluster-up cluster-down cluster-status test-app

cluster-up:
	./infra/scripts/create-cluster.sh

cluster-down:
	./infra/scripts/destroy-cluster.sh

cluster-status:
	kubectl get nodes -o wide
	kubectl get pods -A

test-app:
	kubectl apply -k k8s/platform/test-app
	kubectl -n dreamops get deploy,pods,svc
