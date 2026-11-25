#!/usr/bin/env bash
# Solution de référence : d2-03 — Rolling update avec motif
kubectl config use-context ckad-a
kubectl -n d2-03 set image deploy/front nginx=nginx:1.28-alpine
kubectl -n d2-03 annotate deploy front kubernetes.io/change-cause='passage en 1.28'
kubectl -n d2-03 rollout status deploy/front --timeout=120s
kubectl -n d2-03 rollout history deploy/front
