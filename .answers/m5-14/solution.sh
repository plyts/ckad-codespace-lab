#!/usr/bin/env bash
# Solution de référence : m5-14 — Service ClusterIP
kubectl config use-context ckad-a

kubectl -n m5-14 expose deploy ranking --name=ranking-svc --type=ClusterIP --port=8080 --target-port=5678 \
  --dry-run=client -o yaml > svc.yaml
  kubectl apply -f svc.yaml
