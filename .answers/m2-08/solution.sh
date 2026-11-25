#!/usr/bin/env bash
# Solution de référence : m2-08 — ResourceQuota
kubectl config use-context ckad-a

kubectl -n m2-08 create quota team-quota --hard=pods=4,requests.cpu=800m,requests.memory=512Mi
kubectl -n m2-08 run probe --image=nginx:1.27-alpine --dry-run=client -o yaml > probe.yaml
yq -i '.spec.containers[0].resources = {"requests": {"cpu": "100m", "memory": "64Mi"}}' probe.yaml
kubectl apply -f probe.yaml
kubectl -n m2-08 wait --for=condition=Ready pod/probe --timeout=60s
