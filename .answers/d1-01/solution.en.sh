#!/usr/bin/env bash
# Reference solution: d1-01 — First nginx Pod
kubectl config use-context ckad-a
# Imperative: the fastest in the exam.
kubectl -n d1-01 run web --image=nginx:1.27-alpine --labels=app=web --port=80
kubectl -n d1-01 wait --for=condition=Ready pod/web --timeout=90s
# Manual check:
kubectl -n d1-01 get pod web --show-labels -o wide
# VARIANT: generate the YAML then apply it
#   kubectl -n d1-01 run web --image=nginx:1.27-alpine --labels=app=web --port=80 --dry-run=client -o yaml > web.yaml
#   kubectl apply -f web.yaml
