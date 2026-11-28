#!/usr/bin/env bash
# Reference solution: m5-14 — ClusterIP Service
kubectl config use-context ckad-a

kubectl -n m5-14 expose deploy ranking --name=ranking-svc --type=ClusterIP --port=8080 --target-port=5678 \
  --dry-run=client -o yaml > svc.yaml
  kubectl apply -f svc.yaml
