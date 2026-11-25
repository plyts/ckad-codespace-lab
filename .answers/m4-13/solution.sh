#!/usr/bin/env bash
# Solution de référence : m4-13 — Quota
kubectl config use-context ckad-a

kubectl -n m4-13 create quota team-quota --hard=pods=6,requests.cpu=1,requests.memory=1Gi
kubectl -n m4-13 run probe --image=nginx:1.27-alpine --dry-run=client -o yaml > probe.yaml
yq -i '.spec.containers[0].resources = {"requests": {"cpu": "100m", "memory": "64Mi"}}' probe.yaml
kubectl apply -f probe.yaml
kubectl -n m4-13 wait --for=condition=Ready pod/probe --timeout=60s
