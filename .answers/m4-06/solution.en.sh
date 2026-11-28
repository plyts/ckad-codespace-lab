#!/usr/bin/env bash
# Reference solution: m4-06 — 20% canary
kubectl config use-context ckad-b

kubectl -n m4-06 create deployment pricing-canary --image=hashicorp/http-echo:1.0.0 --replicas=1 \
  --dry-run=client -o yaml -- /http-echo '-text=pricing v2' > canary.yaml
yq -i '.spec.selector.matchLabels = {"app":"pricing","track":"canary"}
       | .spec.template.metadata.labels = {"app":"pricing","track":"canary"}
       | .metadata.labels = {"app":"pricing","track":"canary"}' canary.yaml
kubectl apply -f canary.yaml
kubectl -n m4-06 scale deploy pricing-stable --replicas=4
kubectl -n m4-06 rollout status deploy/pricing-canary --timeout=120s
