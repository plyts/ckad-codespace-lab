#!/usr/bin/env bash
# Solution de référence : d3-05 — ImagePullBackOff
kubectl config use-context ckad-a
kubectl -n d3-05 describe pod -l app=cache | tail -8     # Failed to pull image "redis:7.4-alpinee"
kubectl -n d3-05 set image deploy/cache redis=redis:7.4-alpine
kubectl -n d3-05 rollout status deploy/cache --timeout=120s
