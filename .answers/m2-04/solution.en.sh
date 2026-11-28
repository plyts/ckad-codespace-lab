#!/usr/bin/env bash
# Reference solution: m2-04 — 25% canary
kubectl config use-context ckad-a

kubectl -n m2-04 create deployment search-canary --image=hashicorp/http-echo:1.0.0 --replicas=1 \
  --dry-run=client -o yaml -- /http-echo '-text=search v2' > canary.yaml
yq -i '.spec.selector.matchLabels = {"app":"search","track":"canary"}
       | .spec.template.metadata.labels = {"app":"search","track":"canary"}
       | .metadata.labels = {"app":"search","track":"canary"}' canary.yaml
kubectl apply -f canary.yaml
kubectl -n m2-04 scale deploy search-stable --replicas=3
kubectl -n m2-04 rollout status deploy/search-canary --timeout=120s
