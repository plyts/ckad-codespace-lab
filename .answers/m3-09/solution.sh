#!/usr/bin/env bash
# Solution de référence : m3-09 — ServiceAccount d'un Deployment
kubectl config use-context ckad-b

kubectl -n m3-09 create serviceaccount metrics-reader
kubectl -n m3-09 set serviceaccount deploy/collector metrics-reader
kubectl -n m3-09 rollout status deploy/collector --timeout=120s
