#!/usr/bin/env bash
# Solution de référence : m5-05 — Rolling update
kubectl config use-context ckad-a

kubectl -n m5-05 set image deploy/portal nginx=nginx:1.28-alpine
kubectl -n m5-05 annotate deploy portal kubernetes.io/change-cause='montée de version'
kubectl -n m5-05 scale deploy portal --replicas=4
kubectl -n m5-05 rollout status deploy/portal --timeout=120s
