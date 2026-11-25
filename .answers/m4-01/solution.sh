#!/usr/bin/env bash
# Solution de référence : m4-01 — Pod et manifeste
kubectl config use-context ckad-a

mkdir -p $(dirname ~/ckad/m4-01/edge.yaml)
kubectl -n m4-01 run edge --image=nginx:1.28-alpine --labels=tier=edge,env=prod --port=80 --dry-run=client -o yaml > ~/ckad/m4-01/edge.yaml
kubectl apply -f ~/ckad/m4-01/edge.yaml
kubectl -n m4-01 wait --for=condition=Ready pod/edge --timeout=90s
