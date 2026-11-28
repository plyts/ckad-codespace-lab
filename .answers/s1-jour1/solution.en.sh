#!/usr/bin/env bash
# Reference solution: s1-jour1 — Shop, day 1: deploy v1
kubectl config use-context ckad-a
kubectl -n boutique-j1 create deployment redis --image=redis:7.4-alpine --port=6379
kubectl -n boutique-j1 expose deploy redis --port=6379
kubectl -n boutique-j1 create deployment api --image=hashicorp/http-echo:1.0.0 --replicas=2 --port=5678 \
  -- /http-echo -text='api v1'
kubectl -n boutique-j1 expose deploy api --port=80 --target-port=5678
kubectl -n boutique-j1 create deployment front --image=nginx:1.27-alpine --replicas=2 --port=80
kubectl -n boutique-j1 expose deploy front --port=80
for d in redis api front; do kubectl -n boutique-j1 rollout status deploy/$d --timeout=120s; done
# Equivalent declarative reference: app/boutique/jour1.yaml
