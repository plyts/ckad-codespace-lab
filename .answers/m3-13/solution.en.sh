#!/usr/bin/env bash
# Reference solution: m3-13 — NodePort Service
kubectl config use-context ckad-b

kubectl -n m3-13 expose deploy gateway --name=gateway-svc --type=NodePort --port=80 --target-port=5678 \
  --dry-run=client -o yaml > svc.yaml

yq -i '.spec.ports[0].nodePort = 30180' svc.yaml
  kubectl apply -f svc.yaml
